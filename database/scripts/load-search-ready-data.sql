\copy gwells_well_yield_unit FROM './postgres/well_yield_unit.csv' HEADER DELIMITER ',' CSV
\copy gwells_province_state  FROM './postgres/province_state.csv'  HEADER DELIMITER ',' CSV
\copy gwells_land_district   FROM './postgres/land_district.csv'   HEADER DELIMITER ',' CSV
\copy gwells_well_owner      FROM './postgres/well_owner.csv'      HEADER DELIMITER ',' CSV
\copy gwells_well            FROM './postgres/well.csv'            HEADER DELIMITER ',' CSV
