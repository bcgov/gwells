SET TRIMSPOOL ON
SET ECHO OFF
SET VERIFY OFF
SET TERMOUT OFF
SPOOL H:\xform_gwells_land_district.csv
SELECT /*csv*/  
  SYS_GUID() AS LAND_DISTRICT_GUID,
  TRIM(WELLS.WELLS_LEGAL_LAND_DIST_CODES.LEGAL_LAND_DISTRICT_CODE) AS CODE,
  TRIM(WELLS.WELLS_LEGAL_LAND_DIST_CODES.LEGAL_LAND_DISTRICT_NAME) AS NAME,
  WELLS.WELLS_LEGAL_LAND_DIST_CODES.SORT_ORDER,
  '2017-07-01 00:00:00-08' AS when_created,
  '2017-07-01 00:00:00-08' AS when_updated,
  'ETL_USER' AS who_created,
  'ETL_USER' AS who_updated
FROM WELLS.WELLS_LEGAL_LAND_DIST_CODES
ORDER BY trim(LEGAL_LAND_DISTRICT_NAME)
/
SPOOL OFF

SET TRIMSPOOL ON
SET ECHO OFF
SET VERIFY OFF
SET TERMOUT OFF
SPOOL H:\xform_gwells_backfill_type.csv
SELECT /*csv*/  
  SYS_GUID() AS backfill_type_guid,
  CODE,
  INITCAP(CODE) AS description,
  'N' AS is_hidden,
  ROWNUM * 10 AS SORT_ORDER
FROM (
  SELECT DISTINCT UPPER(TRIM(BACKFILL_MATERIAL)) AS CODE
  FROM WELLS.WELLS_WELLS
  WHERE BACKFILL_MATERIAL IS NOT NULL 
  AND   BACKFILL_MATERIAL NOT IN ('UNKNOWN','UNKNOWN MATERIAL','NONE','NOT APPLICABLE','NOT PROVIDED','N/A')
  ORDER BY UPPER(TRIM(BACKFILL_MATERIAL))
)
ORDER BY CODE
/
SPOOL OFF

SET TRIMSPOOL ON
SET ECHO OFF
SET VERIFY OFF
SET TERMOUT OFF
SPOOL H:\xform_gwells_surface_seal_material.csv
SELECT /*csv*/  
  'ETL_USER' AS who_created,
  '2017-07-01 00:00:00-08' AS when_created,
  'ETL_USER' AS who_updated,
  '2017-07-01 00:00:00-08' AS when_updated,
  SYS_GUID() AS surface_seal_material_guid,
  regexp_replace(
  regexp_replace(
  regexp_replace(
  regexp_replace(
  regexp_replace( 
  regexp_replace(sealant_material,
  'BENTONITE|BENONITE|BETONITE|BEOTNITE|BENTIONITE|BETNONITE|BENT','BT',1,0,'i')
  , 'GROUNT|GROUT|FROUT','GR',1,0,'i')
  , 'CEMENT','CM',1,0,'i')
  , 'SODIUM','NA',1,0,'i')
  , ' INCH','"',1,0,'i')
  , 'CONCRETE','CC',1,0,'i')
  AS CODE,
  INITCAP(SEALANT_MATERIAL) AS description,
  'N' AS is_hidden,
  ROWNUM * 10 AS SORT_ORDER,
  SEALANT_MATERIAL AS SEALANT_MATERIAL  
FROM (
  SELECT DISTINCT UPPER(TRIM(SEALANT_MATERIAL)) AS SEALANT_MATERIAL
  FROM WELLS.WELLS_WELLS
  WHERE SEALANT_MATERIAL IS NOT NULL
  AND SEALANT_MATERIAL != '2007-03-07'
  AND SEALANT_MATERIAL != 'UNKNOWN'
  ORDER BY  UPPER(TRIM(SEALANT_MATERIAL))
)
WHERE LENGTH(
  regexp_replace(
  regexp_replace(
  regexp_replace(
  regexp_replace(
  regexp_replace( 
  regexp_replace(sealant_material,
  'BENTONITE|BENONITE|BETONITE|BEOTNITE|BENTIONITE|BETNONITE|BENT','BT',1,0,'i')
  , 'GROUNT|GROUT|FROUT','GR',1,0,'i')
  , 'CEMENT','CM',1,0,'i')
  , 'SODIUM','NA',1,0,'i')
  , ' INCH','"',1,0,'i')
  , 'CONCRETE','CC',1,0,'i')
) < 11
/
SPOOL OFF








SET TRIMSPOOL ON
SET ECHO OFF
SET VERIFY OFF
SET TERMOUT OFF
SPOOL H:\xform_gwells_surface_seal_method.csv
SELECT /*csv*/  
  'ETL_USER' AS who_created,
  '2017-07-01 00:00:00-08' AS when_created,
  'ETL_USER' AS who_updated,
  '2017-07-01 00:00:00-08' AS when_updated,
  SYS_GUID() AS surface_seal_method_guid,
  CODE AS code,
  INITCAP(CODE) AS description,
  'N' AS is_hidden,
  ROWNUM * 10 AS SORT_ORDER
FROM (
  SELECT DISTINCT UPPER(TRIM(surface_seal_method_code)) AS CODE
  FROM WELLS.WELLS_WELLS
  WHERE surface_seal_method_code != 'UNK'
  ORDER BY  UPPER(TRIM(surface_seal_method_code))
)
/
SPOOL OFF


/*

SELECT DISTINCT WELLS.WELLS_CASINGS.CASING_MATERIAL_CODE, COUNT(*)
FROM WELLS.WELLS_CASINGS
GROUP BY WELLS.WELLS_CASINGS.CASING_MATERIAL_CODE

When converting instance data... 
OPEN_HOLE & UNK (else all)goes to OTHER

"6815ce226c1411e7907ba6006ad3dba0","STEEL","Steel","N","10"
"6815d0ca6c1411e7907ba6006ad3dba0","STL_PUL_OT","Steel Pulled Out","N","20"
"6815d5f26c1411e7907ba6006ad3dba0","PLASTIC","Plastic","N","30"
"6815d7a06c1411e7907ba6006ad3dba0","CEMENT","Cement","N","40"
"6815d8906c1411e7907ba6006ad3dba0","OTHER","Other","N","50"

*/




SET TRIMSPOOL ON
SET ECHO OFF
SET VERIFY OFF
SET TERMOUT OFF
SPOOL H:\xform_gwells_well.csv
SELECT /*csv*/ 
  to_char(WELLS.WELLS_WELLS.WHEN_CREATED,'YYYY-MM-DD HH24:MI:SS') || '-08' /* PST Timezone */ AS created,
  NVL2(WELLS.WELLS_WELLS.WHEN_UPDATED,
      to_char(WELLS.WELLS_WELLS.WHEN_UPDATED,'YYYY-MM-DD HH24:MI:SS') || '-08' /* PST Timezone */,
      NULL) AS modified,
  WELLS.WELLS_WELLS.WELL_TAG_NUMBER,
  SYS_GUID() AS WELL_GUID,
  NVL2(WELLS.WELLS_OWNERS.GIVEN_NAME,WELLS.WELLS_OWNERS.GIVEN_NAME || ' ', NULL) || WELLS.WELLS_OWNERS.SURNAME AS owner_full_name,
   CASE
   WHEN WELLS.WELLS_OWNERS.ADDRESS_LINE IS NULL THEN
     NVL2(WELLS.WELLS_OWNERS.STREET_NUMBER,WELLS.WELLS_OWNERS.STREET_NUMBER || ' ', NULL) || 
     NVL2(WELLS.WELLS_OWNERS.STREET_NAME,WELLS.WELLS_OWNERS.STREET_NAME || ' ', NULL)
   ELSE
      WELLS.WELLS_OWNERS.STREET_NAME
   END AS owner_mailing_address,  
  WELLS.WELLS_OWNERS.CITY AS owner_city,
  WELLS.WELLS_OWNERS.POSTAL_CODE AS owner_postal_code,
  WELLS.WELLS_WELLS.SITE_STREET AS STREET_ADDRESS,
  WELLS.WELLS_WELLS.SITE_AREA AS city,
  WELLS.WELLS_WELLS.LOT_NUMBER AS legal_lot,
  WELLS.WELLS_WELLS.LEGAL_PLAN,
  WELLS.WELLS_WELLS.LEGAL_DISTRICT_LOT,
  WELLS.WELLS_WELLS.LEGAL_BLOCK,
  WELLS.WELLS_WELLS.LEGAL_SECTION,
  WELLS.WELLS_WELLS.LEGAL_TOWNSHIP,
  WELLS.WELLS_WELLS.LEGAL_RANGE,
  WELLS.WELLS_WELLS.PID AS legal_pid,
  WELLS.WELLS_WELLS.WELL_LOCATION AS well_location_description,
  WELLS.WELLS_WELLS.WELL_IDENTIFICATION_PLATE_NO AS identification_plate_number,
  WELLS.WELLS_WELLS.DIAMETER,
  WELLS.WELLS_WELLS.TOTAL_DEPTH_DRILLED,
  WELLS.WELLS_WELLS.DEPTH_WELL_DRILLED AS FINISHED_WELL_DEPTH,
  WELLS.WELLS_WELLS.YIELD_VALUE AS WELL_YIELD,
  WELLS.WELLS_WELLS.WELL_USE_CODE,
  WELLS.WELLS_WELLS.LEGAL_LAND_DISTRICT_CODE,
  CASE
    WHEN WELLS.WELLS_OWNERS.PROVINCE_STATE_CODE = 'BC' THEN 'f46b70b647d411e7a91992ebcb67fe33'
    WHEN WELLS.WELLS_OWNERS.PROVINCE_STATE_CODE = 'AB' THEN 'f46b742647d411e7a91992ebcb67fe33'
    WHEN WELLS.WELLS_OWNERS.PROVINCE_STATE_CODE = 'WASH_STATE' THEN 'f46b77b447d411e7a91992ebcb67fe33'
    ELSE  /* 'OTHER' */ 'f46b7b1a47d411e7a91992ebcb67fe33'
  END AS province_state_guid,
  NVL2 (WELLS.WELLS_WELLS.CLASS_OF_WELL_CODCLASSIFIED_BY,WELLS.WELLS_WELLS.CLASS_OF_WELL_CODCLASSIFIED_BY,'LEGACY') AS CLASS_OF_WELL_CODCLASSIFIED_BY,
  WELLS.WELLS_WELLS.SUBCLASS_OF_WELL_CLASSIFIED_BY,
  CASE
    WHEN WELLS.WELLS_WELLS.YIELD_UNIT_CODE = 'GPM'  THEN 'c4634ef447c311e7a91992ebcb67fe33'
    WHEN WELLS.WELLS_WELLS.YIELD_UNIT_CODE = 'IGM'  THEN 'c4634ff847c311e7a91992ebcb67fe33'
    WHEN WELLS.WELLS_WELLS.YIELD_UNIT_CODE = 'DRY'  THEN 'c46347b047c311e7a91992ebcb67fe33'
    WHEN WELLS.WELLS_WELLS.YIELD_UNIT_CODE = 'LPS'  THEN 'c46350c047c311e7a91992ebcb67fe33'
    WHEN WELLS.WELLS_WELLS.YIELD_UNIT_CODE = 'USGM' THEN 'c463525047c311e7a91992ebcb67fe33'
    WHEN WELLS.WELLS_WELLS.YIELD_UNIT_CODE = 'GPH'  THEN 'c4634b4847c311e7a91992ebcb67fe33'
    WHEN WELLS.WELLS_WELLS.YIELD_UNIT_CODE = 'UNK'  THEN 'c463518847c311e7a91992ebcb67fe33'
    ELSE 'c463518847c311e7a91992ebcb67fe33' /* As PostGres didn't like "" as guid value */
  END AS well_yield_unit_guid,
  WELLS.WELLS_WELLS.DRILLING_METHOD_CODE, /* supersedes CONSTRUCTION_METHOD_CODE */
  WELLS.WELLS_WELLS.LATITUDE,
  CASE
    WHEN WELLS.WELLS_WELLS.LONGITUDE > 0 THEN WELLS.WELLS_WELLS.LONGITUDE * -1
    ELSE WELLS.WELLS_WELLS.LONGITUDE 
  END AS longitude,  
  WELLS.WELLS_WELLS.UTM_NORTH,
  WELLS.WELLS_WELLS.UTM_EAST,
  WELLS.WELLS_WELLS.UTM_ZONE_CODE,
  CASE
     WHEN WELLS.WELLS_WELLS.ORIENTATION_OF_WELL_CODE = 'HORIZ' THEN 'N'
     ELSE 'Y'
  END AS orientation_vertical
FROM WELLS.WELLS_WELLS
LEFT OUTER JOIN WELLS.WELLS_OWNERS
ON WELLS.WELLS_OWNERS.OWNER_ID = WELLS.WELLS_WELLS.OWNER_ID
/
SPOOL OFF


SET TRIMSPOOL ON
SET ECHO OFF
SET VERIFY OFF
SET TERMOUT OFF
SPOOL H:\xform_gwells_driller.csv
SELECT /*csv*/ 
  SYS_GUID() AS driller_guid,
  INITCAP(REGEXP_SUBSTR(CREW_DRILLER_NAME,'(\S*)')) AS first_name,
  INITCAP(REGEXP_SUBSTR(CREW_DRILLER_NAME,'\S+$' )) AS surname,
  PERMIT_NUMBER AS registration_number,
  'N' AS is_hidden,
  WELLS.WELLS_WELLS.DRILLER_COMPANY_CODE
FROM WELLS.WELLS_WELLS 
WHERE ROWID IN (
 SELECT MIN(ROWID)
 FROM WELLS.WELLS_WELLS
 WHERE CREW_DRILLER_NAME IS NOT NULL
 AND   CREW_DRILLER_NAME <> '2015/03/24 2015/03/25'
 AND   PERMIT_NUMBER IS NOT NULL 
 AND   PERMIT_NUMBER <> 'WD'
 AND   DRILLER_COMPANY_CODE IS NOT NULL
 GROUP BY CREW_DRILLER_NAME, PERMIT_NUMBER 
)
/
SPOOL OFF


SET TRIMSPOOL ON
SET ECHO OFF
SET VERIFY OFF
SET TERMOUT OFF
SPOOL H:\xform_gwells_drilling_company.csv
SELECT /*csv*/ 
  SYS_GUID() AS drilling_company_guid,
  WELLS.WELLS_DRILLER_CODES.DRILLER_COMPANY_NAME AS name,
  CASE
     WHEN WELLS.WELLS_DRILLER_CODES.STATUS_FLAG IS NULL THEN 'N'
     WHEN WELLS.WELLS_DRILLER_CODES.STATUS_FLAG = 'N' THEN 'Y'
     WHEN WELLS.WELLS_DRILLER_CODES.STATUS_FLAG = 'Y' THEN 'N'
  END AS is_hidden,  
  WELLS.WELLS_DRILLER_CODES.DRILLER_COMPANY_CODE AS driller_company_code
FROM WELLS.WELLS_DRILLER_CODES
/
SPOOL OFF
