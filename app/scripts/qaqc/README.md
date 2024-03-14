# GWELLS Location Data QA

This suite of scripts is designed to generate Quality Assurance and Quality Control (QAQC) data for all wells registered in the GWELLS system. The primary objective is to build a comprehensive dataset that highlights potential data inconsistencies or issues within existing well records, thereby enabling internal staff to more effectively locate and address these issues.

## Acknowledgements

These scripts have been repurposed and adapted from an existing repository: [smnorris/gwells_locationqa](https://github.com/smnorris/gwells_locationqa).

## Installation/Requirements

1. Create and activate a Python virtual environment:

    ```
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2. Install the required Python packages:

    ```
    pip install -r requirements.txt
    ```

## Download ESA WorldCover 2020

The ESA WorldCover dataset is a crucial component for the script but requires separate downloading. To download and prepare the tiff tiles for British Columbia (BC), ensure you have `awscli` and `gdal` installed and available at the command line. Then, execute the provided bash script:

  ```bash
  ./get_esa_worldcover_bc.sh
  ```

This script is designed for Unix-based systems (`bash`). It can be modified for Windows with minimal changes.

For more information on the ESA WorldCover dataset, visit:

- [ESA WorldCover Website](https://esa-worldcover.org/en)
- [ESA WorldCover Dataset Details](https://esa-worldcover.s3.amazonaws.com/readme.html)

## Usage

The scripts should be run in the following order:

1. **Data Download**:

    Download the required data to the `/data` folder (including GWELLS and PMBC parcel fabric datasets):

    ```python
    python gwells_locationqa.py download
    ```

2. **Reverse Geocoding**:

    Perform reverse-geocoding for all wells. This process has an optional API key and takes approximately 6 hours:

    ```python
    python gwells_locationqa.py geocode <GEOCODER_API_KEY>
    ```

3. **Quality Assurance (QA)**:

    Match well PIDs to PMBC, match addresses, and overlay with agricultural data sources:

    ```python
    python gwells_locationqa.py qa
    ```

4. **Data Extraction**:

   Run the `extract_data.py` script to extract specific columns from the generated `gwells_locationqa.csv` file. This step focuses on key data points for further analysis in GWELLS:

    ```python
    python extract_data.py
    ```

   This script isolates and extracts essential columns such as `well_tag_number`, `distance_geocode`, `distance_to_matching_pid`, `score_address`, `score_city`, and `xref_ind`, saving the refined data into a new file named `extracted_wells_data.csv`. This file is used in a migration to populate the database with this information.

## Output

The output file generated is `gwells_locationqa.csv`, which includes all wells with latitude and longitude data.

The additional columns added to the output file for QAQC purposes are as follows:

| Column                       | Description   |
| ---------------------------- | ------------- |
| nr_district_name             | Natural Resource District |
| nr_region_name               | Natural Resource Region |
| fullAddress                  | Geocoder result |
| streetAddress                | Geocoder results parsed to match GWELLS address |
| civicNumber                  | Geocoder result |
| civicNumberSuffix            | Geocoder result |
| streetName                   | Geocoder result |
| streetType                   | Geocoder result |
| isStreetTypePrefix           | Geocoder result |
| streetDirection              | Geocoder result |
| isStreetDirectionPrefix      | Geocoder result |
| streetQualifier              | Geocoder result |
| localityName                 | Geocoder result |
| distance_geocode             | Distance from well to result of geocode |
| distance_to_matching_pid     | Distance from well to BC Parcel Fabric polygon with matching PID |
| score_address                | Token Set Ratio score for matching well's address to reverse geocoded address |
| score_location_description   | Token Set Ratio score for matching well's location description to reverse geocoded full address |
| score_city                   | Token Set Ratio score for matching well's city to reverse geocoded locality |
| xref_ind                     | Indicates if specific strings found in comments column |
| alr_ind                      | Indicates if the well is within the ALR as defined by relevant datasets |
| btm_label                    | BTM Present Land Use Label at well location |
| esa_landclass                | ESA WorldCover land class at well location |

