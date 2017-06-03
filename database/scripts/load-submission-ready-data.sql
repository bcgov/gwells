\encoding windows-1251
\copy gwells_well_yield_unit 	FROM './postgres/gwells_well_yield_unit.csv' 	HEADER DELIMITER ',' CSV
\copy gwells_province_state  	FROM './postgres/gwells_province_state.csv' 	HEADER DELIMITER ',' CSV
\copy gwells_well_activity_type FROM './postgres/gwells_well_activity_type.csv' HEADER DELIMITER ',' CSV
\copy gwells_intended_water_use	FROM './postgres/gwells_intended_water_use.csv' HEADER DELIMITER ',' CSV
\copy gwells_well_class  		FROM './postgres/gwells_well_class.csv'  		HEADER DELIMITER ',' CSV
\copy gwells_well_subclass   	FROM './postgres/gwells_well_subclass.csv'   	HEADER DELIMITER ',' CSV