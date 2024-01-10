#!/bin/bash
set -euxo pipefail

# create data folder if not present
mkdir -p data

# Download BC tiles of ESA world landcover from S3 bucket
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N54W123_Map.tif data/ESA_WorldCover_10m_2020_v100_N54W123_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N57W120_Map.tif data/ESA_WorldCover_10m_2020_v100_N57W120_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N51W126_Map.tif data/ESA_WorldCover_10m_2020_v100_N51W126_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N57W138_Map.tif data/ESA_WorldCover_10m_2020_v100_N57W138_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N54W132_Map.tif data/ESA_WorldCover_10m_2020_v100_N54W132_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N48W117_Map.tif data/ESA_WorldCover_10m_2020_v100_N48W117_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N57W141_Map.tif data/ESA_WorldCover_10m_2020_v100_N57W141_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N48W120_Map.tif data/ESA_WorldCover_10m_2020_v100_N48W120_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N51W135_Map.tif data/ESA_WorldCover_10m_2020_v100_N51W135_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N51W120_Map.tif data/ESA_WorldCover_10m_2020_v100_N51W120_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N48W132_Map.tif data/ESA_WorldCover_10m_2020_v100_N48W132_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N54W129_Map.tif data/ESA_WorldCover_10m_2020_v100_N54W129_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N54W135_Map.tif data/ESA_WorldCover_10m_2020_v100_N54W135_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N57W135_Map.tif data/ESA_WorldCover_10m_2020_v100_N57W135_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N57W129_Map.tif data/ESA_WorldCover_10m_2020_v100_N57W129_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N51W129_Map.tif data/ESA_WorldCover_10m_2020_v100_N51W129_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N48W129_Map.tif data/ESA_WorldCover_10m_2020_v100_N48W129_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N54W120_Map.tif data/ESA_WorldCover_10m_2020_v100_N54W120_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N54W126_Map.tif data/ESA_WorldCover_10m_2020_v100_N54W126_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N51W123_Map.tif data/ESA_WorldCover_10m_2020_v100_N51W123_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N51W132_Map.tif data/ESA_WorldCover_10m_2020_v100_N51W132_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N57W126_Map.tif data/ESA_WorldCover_10m_2020_v100_N57W126_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N57W132_Map.tif data/ESA_WorldCover_10m_2020_v100_N57W132_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N51W117_Map.tif data/ESA_WorldCover_10m_2020_v100_N51W117_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N48W123_Map.tif data/ESA_WorldCover_10m_2020_v100_N48W123_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N57W123_Map.tif data/ESA_WorldCover_10m_2020_v100_N57W123_Map.tif --no-sign-request
aws s3 cp s3://esa-worldcover/v100/2020/map/ESA_WorldCover_10m_2020_v100_N48W126_Map.tif data/ESA_WorldCover_10m_2020_v100_N48W126_Map.tif --no-sign-request

# merge tiles by building vrt
gdalbuildvrt data/esa_merged.vrt data/ESA_WorldCover_10m_2020_v100_*.tif

# warp data to BC Albers, writing to compressed geotiff
gdalwarp -co COMPRESS=DEFLATE -co PREDICTOR=2 -co NUM_THREADS=ALL_CPUS -t_srs EPSG:3153 data/esa_merged.vrt esa_bc.tif
