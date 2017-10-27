DROP FUNCTION IF EXISTS replicate();
-- Must be run as PostgreSQL admin due to the 'copy' commands in create remote code tables(i.e. psql -d gwells)
CREATE OR REPLACE FUNCTION replicate() RETURNS void AS $$

DECLARE

wells_rows integer;

BEGIN
	raise notice 'Starting replicate() procedure...';

	raise notice '...replicating...';
	PERFORM public.copy_remote_code_tables();
	PERFORM public.populate_xform_gwells_well();
	PERFORM public.populate_gwells_from_xform();

/*
	raise notice 'Preparing replication report ...'

	select count(*) from gwells.well into wells_rows;
	raise notice '... % rows loaded into the main "wells" table', 	wells_rows;
	raise notice 'Finished gwells_replicate() procedure.';
*/
END;
$$ LANGUAGE plpgsql;
