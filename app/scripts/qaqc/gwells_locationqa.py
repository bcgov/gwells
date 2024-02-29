import csv
import logging
import sys
from zipfile import ZipFile, BadZipFile
from io import BytesIO
from time import sleep
import os
from pathlib import Path
import tarfile
import tempfile
from urllib.parse import urlparse
import urllib.request


import fiona
import rasterio
import geopandas as gpd
import pandas as pd
import requests
import click
from thefuzz import fuzz
import bcdata


"""
BC Geocoder ADDRESS API

Overview
https://www2.gov.bc.ca/gov/content/data/geographic-data-services/location-services/geocoder

Specs
https://github.com/bcgov/api-specs/tree/master/geocoder

Developer guide
https://github.com/bcgov/api-specs/blob/master/geocoder/geocoder-developer-guide.md

More
https://www2.gov.bc.ca/assets/gov/data/geographic/location-services/geocoder/understanding_geocoder_results.pdf

Status
https://stats.uptimerobot.com/KZ3Nvh29l1/787375578
"""

# source gwells data file
WELLS_URL = "https://s3.ca-central-1.amazonaws.com/gwells-export/export/v2/gwells.zip"

# bc geocoder endpoint of interest
GEOCODER_ENDPOINT = "https://geocoder.api.gov.bc.ca/sites/nearest.json"
ADDRESS_COLUMNS = [
    "fullAddress",
    "siteName",
    "unitDesignator",
    "unitNumber",
    "unitNumberSuffix",
    "civicNumber",
    "civicNumberSuffix",
    "streetName",
    "streetType",
    "isStreetTypePrefix",
    "streetDirection",
    "isStreetDirectionPrefix",
    "streetQualifier",
    "localityName",
    "localityType",
    "electoralArea",
    "provinceCode",
    "locationPositionalAccuracy",
    "locationDescriptor",
    "siteID",
    "blockID",
    "fullSiteDescriptor",
    "accessNotes",
    "siteStatus",
    "siteRetireDate",
    "changeDate",
    "isOfficial",
    "distance",
]

PARCELFABRIC_URL = "https://pub.data.gov.bc.ca/datasets/4cf233c2-f020-4f7a-9b87-1923252fbc24/pmbc_parcel_fabric_poly_svw.zip"

WELLS_FILENAME = "wells.csv"
PIDMATCH_FILENAME = "pidmatch.csv"
EPSG_3154 = "EPSG:3153"


LOG = logging.getLogger(__name__)


class ZipCompatibleTarFile(tarfile.TarFile):
    """
    Wrapper around TarFile to make it more compatible with ZipFile
    Modified from https://github.com/OpenBounds/Processing/blob/master/utils.py
    """

    def infolist(self):
        members = self.getmembers()
        for m in members:
            m.filename = m.name
        return members

    def namelist(self):
        return self.getnames()


def get_compressed_file_wrapper(path):
    """From https://github.com/OpenBounds/Processing/blob/master/utils.py"""
    ARCHIVE_FORMAT_ZIP = "zip"
    ARCHIVE_FORMAT_TAR = "tar"
    ARCHIVE_FORMAT_TAR_GZ = "tar.gz"
    ARCHIVE_FORMAT_TAR_BZ2 = "tar.bz2"
    archive_format = None
    if path.endswith(".zip"):
        archive_format = ARCHIVE_FORMAT_ZIP
    elif path.endswith(".tar.gz") or path.endswith(".tgz"):
        archive_format = ARCHIVE_FORMAT_TAR_GZ
    elif path.endswith(".tar.bz2"):
        archive_format = ARCHIVE_FORMAT_TAR_BZ2
    else:
        try:
            with ZipFile(path, "r"):
                archive_format = ARCHIVE_FORMAT_ZIP
        except BadZipFile:
            try:
                with tarfile.TarFile.open(path, "r"):
                    archive_format = ARCHIVE_FORMAT_TAR
            except tarfile.TarError:
                pass
    if archive_format is None:
        raise Exception("Unable to determine archive format")

    if archive_format == ARCHIVE_FORMAT_ZIP:
        return ZipFile(path, "r")

    elif archive_format == ARCHIVE_FORMAT_TAR_GZ:
        return ZipCompatibleTarFile.open(path, "r:gz")

    elif archive_format == ARCHIVE_FORMAT_TAR_BZ2:
        return ZipCompatibleTarFile.open(path, "r:bz2")


def download_file(url, out_path, filename):
    """Download and extract a zipfile to unique location"""
    out_file = os.path.join(out_path, filename)
    if not os.path.exists(os.path.join(out_path, filename)):
        LOG.info("Downloading " + url)
        parsed_url = urlparse(url)
        urlfile = parsed_url.path.split("/")[-1]
        _, extension = os.path.split(urlfile)
        fp = tempfile.NamedTemporaryFile("wb", suffix=extension, delete=False)
        if parsed_url.scheme == "http" or parsed_url.scheme == "https":
            res = requests.get(url, stream=True)
            if not res.ok:
                raise IOError

            for chunk in res.iter_content(1024):
                fp.write(chunk)
        elif parsed_url.scheme == "ftp":
            dl = urllib.request.urlopen(url)
            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = dl.read(block_sz)
                if not buffer:
                    break
                file_size_dl += len(buffer)
                fp.write(buffer)
        fp.close()
        # extract zipfile
        Path(out_path).mkdir(parents=True, exist_ok=True)
        LOG.info("Extracting %s to %s" % (fp.name, out_path))
        zipped_file = get_compressed_file_wrapper(fp.name)
        zipped_file.extractall(out_path)
        zipped_file.close()
    layer = fiona.listlayers(os.path.join(out_path, filename))[0]
    return (out_file, layer)


def get_gwells(outfile=os.path.join("data", WELLS_FILENAME)):
    """
    - get wells csv if not already present
    - retain only records of interest
    - write to file
    - return wells as dataframe
    """
    if os.path.exists(outfile):
        LOG.info(f"Loading {outfile}")
        return pd.read_csv(outfile)
    else:
        r = requests.get(WELLS_URL)
        zip_file = ZipFile(BytesIO(r.content))
        dfs = {
            text_file.filename: pd.read_csv(zip_file.open(text_file.filename))
            for text_file in zip_file.infolist()
            if text_file.filename.endswith(".csv")
        }
        # only retain records with coordinates
        df = dfs["well.csv"].dropna(subset=["latitude_Decdeg", "longitude_Decdeg"])
        # only retain records that are unlicensed
        # (we presume locations of licensed wells are correct)
        # df = df[df["licenced_status_code"] == "UNLICENSED"]

        # save as intermediate file
        df.to_csv(outfile, index=False)
        return df


def reverse_geocode(
    x,
    y,
    geocoder_api_key,
    distance_start=200,
    distance_increment=200,
    distance_max=2000,
):
    """
    Provided a location as x/y coordinates (EPSG:4326), request an address
    from BC Geocoder within given distance_start (metres)

    If no result is found, request using an expanding search radius in
    distance_increment steps, until distance_max is reached.

    A dict with 'distance' = 99999 is returned if no result is found.

    This could sped up by:
    - just make the request using the max distance and derive distance between
      source point and returned location
    - make requests either in parallel or async

    """
    result = False
    distance = distance_start
    # expand the search distance until we get a result or hit the max distance
    while result is False and distance <= distance_max:
        params = {
            "point": str(x) + "," + str(y),
            "apikey": geocoder_api_key,
            "outputFormat": "json",
            "maxDistance": distance,
        }
        r = requests.get(GEOCODER_ENDPOINT, params=params)
        LOG.debug(r.request.url)

        # pause for 2s per request if near limit of 1000 requests/min
        if int(r.headers["RateLimit-Remaining"]) < 30:
            LOG.info("Approaching API limit, sleeping for 2 seconds to refresh.")
            sleep(2)
        if r.status_code == 200:
            result = True
        else:
            distance = distance + distance_increment
    if r.status_code == 200:
        address = r.json()["properties"]
        address["distance"] = distance
        return address
    else:
        empty_result = dict([(k, "") for k in ADDRESS_COLUMNS])
        empty_result["distance"] = 99999
        return empty_result


def pidmatch(wells_gdf):
    if os.path.exists(os.path.join("data", PIDMATCH_FILENAME)):
        LOG.info(
            "Loading data/pidmatch.csv, cached result of wells/parcels PID matching"
        )
        pid_distances = gpd.read_file(os.path.join("data", PIDMATCH_FILENAME))
        pid_distances["well_tag_number"] = pid_distances["well_tag_number"].astype(int)

    else:
        # load parcel data
        LOG.info("Loading data/pmbc_parcel_fabric_poly_svw.gdb")
        parcels = gpd.read_file(
            os.path.join("data", "pmbc_parcel_fabric_poly_svw.gdb"),
            layer="pmbc_parcel_fabric_poly_svw",
        )
        # ------
        # ** PID matching **
        # Derive 'distance_to_matching_pid', the distance from well to parcel
        # polygon with the same PID
        # ------
        # get well records with PID values
        wells_with_pid = wells_gdf[wells_gdf["legal_pid"].notna()][
            ["well_tag_number", "legal_pid", "geometry"]
        ]
        # join to parcel fabric on PID
        wells_parcels_pid = pd.merge(
            wells_with_pid, 
            parcels, 
            how="inner", 
            left_on="legal_pid", 
            right_on="PID",
            validate="many_to_one"
        )
        # find distance from well point to parcel polygon with matching PID
        distances_series = wells_parcels_pid["geometry_x"].distance(
            wells_parcels_pid["geometry_y"], align=True
        )
        # put distance values back into merged df but keep just columns of interest
        pid_distances = wells_parcels_pid.assign(
            distance_to_matching_pid=distances_series
        )[["well_tag_number", "distance_to_matching_pid"]]
        # dump to file
        pid_distances.to_csv(os.path.join("data", PIDMATCH_FILENAME), index=False)

    return pd.merge(wells_gdf, pid_distances, on="well_tag_number", how="left")


def agriculture_overlays(in_gdf):
    """Overlay wells with several definitions of agricultural lands or a proxy:
    - BTM
    - ALR
    - ESA land cover
    """
    if os.path.exists(os.path.join("data", "agriculture_overlays.csv")):
        LOG.info(
            "Loading data/agriculture_overlays.csv, cached result of ALR/BTM/ESA overlays"
        )
        ag_overlays = gpd.read_file(os.path.join("data", "agriculture_overlays.csv"))
        ag_overlays["well_tag_number"] = ag_overlays["well_tag_number"].astype(int)

    else:
        LOG.info("Overlaying wells with ALR")
        alr = (
            bcdata.get_data("WHSE_LEGAL_ADMIN_BOUNDARIES.OATS_ALR_POLYS", as_gdf=True)[
                ["STATUS", "geometry"]
            ]
            .to_crs(EPSG_3154)
            .rename(
                columns={
                    "STATUS": "alr_ind",
                }
            )
        )
        alr_overlay = gpd.sjoin(in_gdf, alr, how="left", predicate="within")
        alr_overlay = alr_overlay[["well_tag_number", "alr_ind"]]

        LOG.info("Overlaying wells with BTM")
        btm = (
            bcdata.get_data(
                "WHSE_BASEMAPPING.BTM_PRESENT_LAND_USE_V1_SVW", as_gdf=True
            )[["PRESENT_LAND_USE_LABEL", "geometry"]]
            .to_crs(EPSG_3154)
            .rename(
                columns={
                    "PRESENT_LAND_USE_LABEL": "btm_label",
                }
            )
        )
        btm_overlay = gpd.sjoin(in_gdf, btm, how="left", predicate="within")
        btm_overlay = btm_overlay[["well_tag_number", "btm_label"]]

        # overlay input with ESA land cover
        LOG.info("Overlaying wells with ESA 10m landcover (2020)")
        landclass_lookup = {
            0: "NULL",
            10: "Tree cover",
            20: "Shrubland",
            30: "Grassland",
            40: "Cropland",
            50: "Built-up",
            60: "Bare/sparse vegetation",
            70: "Snow and ice",
            80: "Permanent water bodies",
            90: "Herbaceous wetland",
            95: "Mangroves",
            100: "Moss and lichen",
        }
        esa = in_gdf.copy()
        esa.index = range(len(in_gdf))
        coords = [(x, y) for x, y in zip(esa.geometry.x, in_gdf.geometry.y)]
        raster = rasterio.open("data/esa_bc.tif")
        esa["esa_landclass"] = [landclass_lookup[x[0]] for x in raster.sample(coords)]
        esa = esa[["well_tag_number", "esa_landclass"]]

        # join all three dfs together
        a = pd.merge(alr_overlay, btm_overlay, "left", on="well_tag_number")
        b = pd.merge(a, esa, "left", on="well_tag_number")

        # make sure we only have columns of interest
        ag_overlays = b[["well_tag_number", "alr_ind", "btm_label", "esa_landclass"]]

        # write to csv
        ag_overlays.to_csv("data/agriculture_overlays.csv")

    return ag_overlays


def compare_strings(x):
    return fuzz.token_set_ratio(x[0], x[1])


@click.group()
def cli():
    """
    This is the main command group for the CLI.

    The function `cli` is decorated with `@click.group()`, which turns it into a command group. 
    This group will serve as the base for nesting other sub-commands. The `pass` statement is used 
    here because the function itself does not need to execute any code. Its primary purpose is to 
    serve as a foundation for the CLI structure. Sub-commands will be attached to this group, 
    and they will be the ones performing the actual operations or functionalities.
    """
    pass


@cli.command()
def download():
    """Download required data to data folder"""
    Path("data").mkdir(parents=True, exist_ok=True)
    get_gwells(os.path.join("data", WELLS_FILENAME))
    download_file(PARCELFABRIC_URL, "data", "pmbc_parcel_fabric_poly_svw.gdb")


@cli.command()
@click.argument("geocoder_api_key", envvar="GEOCODER_API_KEY")
@click.option(
    "--out_file",
    "-o",
    default=os.path.join("data", "wells_geocoded.csv"),
    help="Name of output file.",
)
def geocode(geocoder_api_key, out_file):
    """Reverse geocode well locations with BC Geocoder API"""
    # only process if output file does not already exist
    if not os.path.exists(out_file):
        # get wells csv as pandas dataframe
        df = get_gwells(os.path.join("data", WELLS_FILENAME))

        # extract just id and coords
        well_locations = df[
            ["well_tag_number", "longitude_Decdeg", "latitude_Decdeg"]
        ].to_dict("records")

        LOG.info("Reverse geocoding well locations")
        with open(out_file, "w", newline="") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=ADDRESS_COLUMNS + ["well_tag_number"]
            )
            writer.writeheader()
            with click.progressbar(well_locations) as bar:
                for row in bar:
                    r = reverse_geocode(
                        row["longitude_Decdeg"],
                        row["latitude_Decdeg"],
                        geocoder_api_key,
                    )
                    r["well_tag_number"] = row["well_tag_number"]
                    writer.writerow(r)


@cli.command()
def qa():
    """Create several columns to use for location QA
    - distance from well pt to parcel with matching PID
    - wells street address / geocoder street address similarity
    - wells location description / geocoder streeet address similarity
    - wells city / geocoder locality similarity

    While running the analysis, reports on a few counts.
    """
    # load source wells data
    gwells_df = get_gwells()

    # create a copy
    wells_copy = gwells_df.copy()
    wells = gpd.GeoDataFrame(
        wells_copy,
        geometry=gpd.points_from_xy(
            x=wells_copy.longitude_Decdeg, y=wells_copy.latitude_Decdeg, crs="EPSG:4326"
        ),
    ).to_crs(EPSG_3154)
    # convert id to integer
    wells["well_tag_number"] = wells["well_tag_number"].astype(int)
    # retain just columns of interest
    wells = wells[
        [
            "well_tag_number",
            "street_address",
            "city",
            "well_location_description",
            "legal_pid",
            "geometry",
        ]
    ]

    # get NR regions/districts
    nrd = (
        bcdata.get_data("WHSE_ADMIN_BOUNDARIES.ADM_NR_DISTRICTS_SPG", as_gdf=True)[
            ["DISTRICT_NAME", "REGION_ORG_UNIT_NAME", "geometry"]
        ]
        .to_crs(EPSG_3154)
        .rename(
            columns={
                "DISTRICT_NAME": "nr_district_name",
                "REGION_ORG_UNIT_NAME": "nr_region_name",
            }
        )
    )
    # overlay with wells
    wells_nrd = gpd.sjoin(wells, nrd, how="left", predicate="within")

    # load geocode results as string, retain only columns of interest
    geocode_df = pd.read_csv(os.path.join("data", "wells_geocoded.csv"), dtype=str)[
        [
            "well_tag_number",
            "fullAddress",
            "civicNumber",
            "civicNumberSuffix",
            "streetName",
            "streetType",
            "isStreetTypePrefix",
            "streetDirection",
            "isStreetDirectionPrefix",
            "streetQualifier",
            "localityName",
            "distance",
        ]
    ].rename(columns={"distance": "distance_geocode"})
    # convert tag and distance_geocode to integer
    geocode_df["well_tag_number"] = geocode_df["well_tag_number"].astype(int)
    geocode_df["distance_geocode"] = geocode_df["distance_geocode"].astype(int)

    # combine wells and geocode results
    wells_nrd_geocoded = pd.merge(wells_nrd, geocode_df, "inner", on="well_tag_number")

    # match wells pid values to parcels pid values
    wells_nrd_geocoded_pidmatched = pidmatch(wells_nrd_geocoded)

    scoring = wells_nrd_geocoded_pidmatched  # shorter name

    # ------
    # ** Address matching **
    # ------
    LOG.info("Generating address matching scores")

    # before trying matching, clean the addresses by filling in nulls and
    # do some very simple string standardization
    scoring["street_address"] = scoring["street_address"].fillna("")
    scoring["well_location_description"] = scoring["well_location_description"].fillna(
        ""
    )
    scoring["city"] = scoring["city"].fillna("")
    # lowercasify the scoring address strings
    scoring["street_address"] = scoring["street_address"].str.lower()
    # abbreviate road types to match geocoder
    street_abbreviations = {
        "road": "rd",
        "drive": "dr",
        "avenue": "ave",
        "highway": "hwy",
        "street": "st",
        "boulevard": "blvd",
        "crescent": "cres",
        "frontage": "frtg",
        "place": "pl",
        "court": "crt",
        "terrace": "terr",
        "lookout": "lkout",
        "heights": "hts",
    }
    for k in street_abbreviations:
        scoring["street_address"] = scoring["street_address"].str.replace(
            k, street_abbreviations[k]
        )
    # combine geocoder number/name/type/direction into a single slug
    t = scoring[["civicNumber", "streetName", "streetType", "streetDirection"]]
    scoring["streetAddress"] = t.apply(
        lambda x: " ".join(x.dropna().astype(str).values), axis=1
    )

    #
    # "score_address"
    #
    # compares gwells address to geocoder address
    t = scoring[["street_address", "streetAddress"]]
    scoring["score_address"] = t.apply(compare_strings, axis=1)

    #
    # "score_location_description"
    #
    # compares well_location_description with geocoder full street address
    t = scoring[["well_location_description", "fullAddress"]]
    scoring["score_location_description"] = t.apply(compare_strings, axis=1)

    #
    # "city_score"
    #
    # compares gwells city to geocoder locality
    t = scoring[["city", "localityName"]]
    scoring["score_city"] = t.apply(compare_strings, axis=1)

    # extract only columns of interest
    scoring = scoring[
        [
            "well_tag_number",
            "nr_district_name",
            "nr_region_name",
            "fullAddress",
            "streetAddress",
            "civicNumber",
            "civicNumberSuffix",
            "streetName",
            "streetType",
            "isStreetTypePrefix",
            "streetDirection",
            "isStreetDirectionPrefix",
            "streetQualifier",
            "localityName",
            "distance_geocode",
            "distance_to_matching_pid",
            "score_address",
            "score_location_description",
            "score_city",
        ]
    ]

    # Join the NR/geocoding/pidmatch scoring df back to source wells
    out_df = pd.merge(gwells_df, scoring, "left", on="well_tag_number")

    # addtional QA -
    # find records that have been cross referenced
    # (fuzzy match scoring doesn't seem appropriate here, we can just
    # search for exact matches of several permutations to catch most)
    out_df["xref_ind"] = (
        out_df["comments"]
        .str.upper()
        .fillna("")
        .str.contains("CROSS R|CROSS-R|REF'D|REFERENCED|REFD|XREF|X-R|X R")
    )

    # finally, overlay with ALR/BTM/ESA Landcover to find wells in agricultural areas
    # ag_overlays = agriculture_overlays(wells)
    # out_df = pd.merge(out_df, ag_overlays, "left", on="well_tag_number")

    # and dump results to file
    LOG.info("Writing output file gwells_locationqa.csv")
    out_df.to_csv("gwells_locationqa.csv", index=False)


if __name__ == "__main__":
    cli()
