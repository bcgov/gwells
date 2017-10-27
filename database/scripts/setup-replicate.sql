
--  Run this script as gwells owner (e.g. psql -d gwells -U userGN0)

DROP FUNCTION IF EXISTS setup_replicate();

CREATE OR REPLACE FUNCTION setup_replicate() RETURNS void AS $$
BEGIN
	raise notice 'Starting setup_replicate() procedure...';
	PERFORM public.clear_tables();
	PERFORM public.create_xform_well_gwells_ETL_table();
	raise notice 'Finished setup_replicate() procedure.';
END;
$$ LANGUAGE plpgsql;
