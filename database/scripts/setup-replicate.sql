
--  Run this script as gwells owner (e.g. psql -d gwells -U userGN0)

DROP FUNCTION IF EXISTS setup_replicate();

CREATE OR REPLACE FUNCTION setup_replicate() RETURNS void AS $$
BEGIN
	raise notice 'Starting setup_replicate() procedure...';
	PERFORM public.clear_tables();
	PERFORM public.copy_remote_code_tables();
	raise notice 'Finished setup_replicate() procedure.';
END;
$$ LANGUAGE plpgsql;
