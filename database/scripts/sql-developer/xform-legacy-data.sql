SET ECHO OFF
SET VERIFY OFF
SPOOL H:\tmp\land_district.csv

SELECT /*csv*/ CAST(WELLS.WELLS_LEGAL_LAND_DIST_CODES.LEGAL_LAND_DISTRICT_CODE AS INTEGER) AS ID,
  TRIM(WELLS.WELLS_LEGAL_LAND_DIST_CODES.LEGAL_LAND_DISTRICT_CODE) AS CODE,
  TRIM(WELLS.WELLS_LEGAL_LAND_DIST_CODES.LEGAL_LAND_DISTRICT_NAME) AS NAME,
/*
  WELLS.WELLS_LEGAL_LAND_DIST_CODES.STATUS_FLAG,
  WELLS.WELLS_LEGAL_LAND_DIST_CODES.WHO_CREATED,
  WELLS.WELLS_LEGAL_LAND_DIST_CODES.WHEN_CREATED,
  WELLS.WELLS_LEGAL_LAND_DIST_CODES.WHO_UPDATED,
  WELLS.WELLS_LEGAL_LAND_DIST_CODES.WHEN_UPDATED,
*/  
  WELLS.WELLS_LEGAL_LAND_DIST_CODES.SORT_ORDER
FROM WELLS.WELLS_LEGAL_LAND_DIST_CODES
ORDER BY trim(LEGAL_LAND_DISTRICT_NAME)
/

SPOOL OFF


SET ECHO OFF
SET VERIFY OFF
SPOOL H:\tmp\well_owner.csv

SELECT /*csv*/ WELLS.WELLS_OWNERS.OWNER_ID AS ID,
  NVL2(WELLS.WELLS_OWNERS.GIVEN_NAME,WELLS.WELLS_OWNERS.GIVEN_NAME || ' ', NULL) || WELLS.WELLS_OWNERS.SURNAME AS FULL_NAME,
/*
  WELLS.WELLS_OWNERS.WHO_CREATED,
  WELLS.WELLS_OWNERS.WHEN_CREATED,
 */ 
   CASE
	 WHEN WELLS.WELLS_OWNERS.ADDRESS_LINE IS NULL THEN
	   NVL2(WELLS.WELLS_OWNERS.STREET_NUMBER,WELLS.WELLS_OWNERS.STREET_NUMBER || ' ', NULL) || 
	   NVL2(WELLS.WELLS_OWNERS.STREET_NAME,WELLS.WELLS_OWNERS.STREET_NAME || ' ', NULL)
	 ELSE
  		WELLS.WELLS_OWNERS.STREET_NAME
   END AS STREET_ADDRESS,  
  WELLS.WELLS_OWNERS.CITY,
  WELLS.WELLS_OWNERS.POSTAL_CODE,
  WELLS.WELLS_OWNERS.PHONE_NUMBER,
 /* 
  WELLS.WELLS_OWNERS.WHO_UPDATED,
  WELLS.WELLS_OWNERS.WHEN_UPDATED, */
  WELLS.WELLS_OWNERS.EMAIL_ADDRESS,
  CASE
	WHEN WELLS.WELLS_OWNERS.PROVINCE_STATE_CODE = 'BC' THEN 102
	WHEN WELLS.WELLS_OWNERS.PROVINCE_STATE_CODE = 'AB' THEN 103
	WHEN WELLS.WELLS_OWNERS.PROVINCE_STATE_CODE = 'WASH_STATE' THEN 104
	WHEN WELLS.WELLS_OWNERS.PROVINCE_STATE_CODE = 'OTHER' THEN 105
	ELSE 105
  END AS GWELLS_PROVINCE_STATE_ID
FROM WELLS.WELLS_OWNERS
ORDER BY WELLS.WELLS_OWNERS.OWNER_ID
/

SPOOL OFF


SET ECHO OFF
SET VERIFY OFF
SPOOL H:\tmp\well.csv


SELECT /*csv*/ WELLS.WELLS_WELLS.WELL_ID AS ID,
  WELLS.WELLS_WELLS.SITE_STREET AS STREET_ADDRESS,
  WELLS.WELLS_WELLS.SITE_AREA,
  WELLS.WELLS_WELLS.LOT_NUMBER,
  WELLS.WELLS_WELLS.LEGAL_PLAN,
  WELLS.WELLS_WELLS.LEGAL_DISTRICT_LOT,
  WELLS.WELLS_WELLS.PID,
  WELLS.WELLS_WELLS.WELL_IDENTIFICATION_PLATE_NO AS IDENTIFICATION_PLATE_NUMBER,
  WELLS.WELLS_WELLS.DIAMETER,
  WELLS.WELLS_WELLS.TOTAL_DEPTH_DRILLED AS WELL_DRILLED_DEPTH,
  WELLS.WELLS_WELLS.YIELD_VALUE,
  WELLS.WELLS_WELLS.OWNER_ID AS GWELLS_WELL_OWNER_ID,
  CASE
    WHEN WELLS.WELLS_WELLS.YIELD_UNIT_CODE = 'GPM'  THEN 2
    WHEN WELLS.WELLS_WELLS.YIELD_UNIT_CODE = 'IGM'  THEN 3
    WHEN WELLS.WELLS_WELLS.YIELD_UNIT_CODE = 'DRY'  THEN 7
    WHEN WELLS.WELLS_WELLS.YIELD_UNIT_CODE = 'LPS'  THEN 4
    WHEN WELLS.WELLS_WELLS.YIELD_UNIT_CODE = 'USGM' THEN 6
    WHEN WELLS.WELLS_WELLS.YIELD_UNIT_CODE = 'GPH'  THEN 1
    WHEN WELLS.WELLS_WELLS.YIELD_UNIT_CODE = 'UNK'  THEN 5
    ELSE NULL
  END AS GWELLS_WELL_UNIT_ID,
  WELLS.WELLS_WELLS.WELL_TAG_NUMBER,
  WELLS.WELLS_WELLS.DEPTH_WELL_DRILLED AS FINISHED_WELL_DEPTH,
  WELLS.WELLS_WELLS.LEGAL_LAND_DISTRICT_CODE AS GWELLS_LAND_DISTRICT_ID  
/*  
  WELLS.WELLS_WELLS.SEQUENCE_NO,
  WELLS.WELLS_WELLS.DRILLER_WELL_ID,
  WELLS.WELLS_WELLS.WELL_USE_CODE,
  WELLS.WELLS_WELLS.UTM_ACCURACY_CODE,
  WELLS.WELLS_WELLS.LOC_ACCURACY_CODE,
  WELLS.WELLS_WELLS.CONSTRUCTION_START_DATE,
  WELLS.WELLS_WELLS.MS_ACCESS_NUM_OF_WELL,
  WELLS.WELLS_WELLS.CONSTRUCTION_END_DATE,
  WELLS.WELLS_WELLS.DATE_ENTERED,
  WELLS.WELLS_WELLS.DRILLING_METHOD_CODE,
  WELLS.WELLS_WELLS.RIG_NUMBER,
  WELLS.WELLS_WELLS.CREW_HELPER_NAME,
  WELLS.WELLS_WELLS.LITHOLOGY_MEASURMENT_UNIT,
  WELLS.WELLS_WELLS.OLD_WELL_NUMBER,
  WELLS.WELLS_WELLS.OLD_MAPSHEET,
  WELLS.WELLS_WELLS.CREW_DRILLER_NAME,
  WELLS.WELLS_WELLS.WATER_UTILITY_FLAG,
  WELLS.WELLS_WELLS.SITE_ISLAND,
  WELLS.WELLS_WELLS.LEGAL_TOWNSHIP,
  WELLS.WELLS_WELLS.LEGAL_SECTION,
  WELLS.WELLS_WELLS.LEGAL_RANGE,
  WELLS.WELLS_WELLS.INDIAN_RESERVE,
  WELLS.WELLS_WELLS.MERIDIAN,
  WELLS.WELLS_WELLS.LEGAL_BLOCK,
  WELLS.WELLS_WELLS.QUARTER,
  WELLS.WELLS_WELLS.LEGAL_MISCELLANEOUS,
  WELLS.WELLS_WELLS.ELEVATION,
  WELLS.WELLS_WELLS.LOCATION_ACCURACY,
  WELLS.WELLS_WELLS.CERTIFICATION,
  WELLS.WELLS_WELLS.BEDROCK_DEPTH,
  WELLS.WELLS_WELLS.WATER_DEPTH,
  WELLS.WELLS_WELLS.PUMP_DESCRIPTION,
  WELLS.WELLS_WELLS.CHEMISTRY_LAB_DATA,
  WELLS.WELLS_WELLS.FIELD_LAB_DATA,
  WELLS.WELLS_WELLS.OWNERS_WELL_NUMBER,
  WELLS.WELLS_WELLS.PERMIT_NUMBER,
  WELLS.WELLS_WELLS.WELL_LOCATION,
  WELLS.WELLS_WELLS.WELL_SEQUENCE_NO,
  WELLS.WELLS_WELLS.CLASS_OF_WELL_CODE,
  WELLS.WELLS_WELLS.SUBCLASS_OF_WELL_CODE,
  WELLS.WELLS_WELLS.ORIENTATION_OF_WELL_CODE,
  WELLS.WELLS_WELLS.STATUS_OF_WELL_CODE,
  WELLS.WELLS_WELLS.LATITUDE,
  WELLS.WELLS_WELLS.LONGITUDE,
  WELLS.WELLS_WELLS.DRILLER_COMPANY_CODE,
  WELLS.WELLS_DRILLER_CODES.DRILLER_COMPANY_NAME,
  WELLS.WELLS_WELLS.CONSTRUCTION_METHOD_CODE,
  WELLS.WELLS_WELLS.BCGS_ID,
  WELLS.WELLS_BCGS_NUMBERS.BCGS_NUMBER,
  WELLS.WELLS_LEGAL_LAND_DIST_CODES.LEGAL_LAND_DISTRICT_NAME,  
  WELLS.WELLS_WELLS.AQUIFER_LITHOLOGY_CODE,
  WELLS.WELLS_AQUIFER_LITHOLOGY_CODES.AQUIFER_LITHOLOGY_NAME,
  WELLS.WELLS_WELLS.WATERSHED_CODE,
  WELLS.WELLS_WATERSHED_CODES.WATERSHED_DESCRIPTION */
FROM WELLS.WELLS_WELLS
LEFT OUTER JOIN WELLS.WELLS_LEGAL_LAND_DIST_CODES
ON WELLS.WELLS_LEGAL_LAND_DIST_CODES.LEGAL_LAND_DISTRICT_CODE = WELLS.WELLS_WELLS.LEGAL_LAND_DISTRICT_CODE
LEFT OUTER JOIN WELLS.WELLS_DRILLER_CODES
ON WELLS.WELLS_DRILLER_CODES.DRILLER_COMPANY_CODE = WELLS.WELLS_WELLS.DRILLER_COMPANY_CODE
LEFT OUTER JOIN WELLS.WELLS_CONSTR_METHOD_CODES
ON WELLS.WELLS_CONSTR_METHOD_CODES.CONSTRUCTION_METHOD_CODE = WELLS.WELLS_WELLS.CONSTRUCTION_METHOD_CODE
LEFT OUTER JOIN WELLS.WELLS_BCGS_NUMBERS
ON WELLS.WELLS_BCGS_NUMBERS.BCGS_ID = WELLS.WELLS_WELLS.BCGS_ID
LEFT OUTER JOIN WELLS.WELLS_AQUIFER_LITHOLOGY_CODES
ON WELLS.WELLS_AQUIFER_LITHOLOGY_CODES.AQUIFER_LITHOLOGY_CODE = WELLS.WELLS_WELLS.AQUIFER_LITHOLOGY_CODE
LEFT OUTER JOIN WELLS.WELLS_WATERSHED_CODES
ON WELLS.WELLS_WATERSHED_CODES.WATERSHED_CODE = WELLS.WELLS_WELLS.WATERSHED_CODE
/
SPOOL OFF

