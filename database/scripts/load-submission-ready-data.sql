\encoding windows-1251
\copy gwells_well_yield_unit FROM './postgres/gwells_province_state.csv' 		HEADER DELIMITER ',' CSV
\copy gwells_province_state  FROM './postgres/gwells_well_activity_type.csv'  	HEADER DELIMITER ',' CSV
\copy gwells_land_district   FROM './postgres/gwells_well_class.csv'   			HEADER DELIMITER ',' CSV
\copy gwells_well_owner      FROM './postgres/gwells_well_subclass.csv'      	HEADER DELIMITER ',' CSV
\copy gwells_well            FROM './postgres/gwells_intended_water_use.csv'  	HEADER DELIMITER ',' CSV
\copy gwells_well            FROM './postgres/gwells_well_yield_unit.csv'    	HEADER DELIMITER ',' CSV