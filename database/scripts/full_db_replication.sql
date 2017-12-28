DROP FUNCTION IF EXISTS gwells_full_replicate();

/*** NOTE: There is no refresh of Code Tables, as that is done during GWELLS Application code deployment
		   This driver SQL script is meant to be run from the Database Pod, during nightly replications,
		   not as part of an application deployment.

		   Therefore, there is a dependency on having all code tables populated, including BCGS numbers.

	export PGPASSWORD=$DATABASE_PASSWORD
	psql -h $DATABASE_SERVICE_NAME -d $DATABASE_NAME -U $DATABASE_USER -c 'SELECT gwells_full_replicate();'

 ***/
CREATE OR REPLACE FUNCTION gwells_full_replicate() RETURNS void AS $$
BEGIN
	TRUNCATE TABLE gwells_well CASCADE;
	PERFORM gwells_populate_xform(false);
	PERFORM gwells_populate_well();	
	PERFORM gwells_migrate_screens();
	PERFORM gwells_migrate_production();
	PERFORM gwells_migrate_casings();
	PERFORM gwells_migrate_perforations();
	PERFORM gwells_migrate_aquifers();
	PERFORM gwells_migrate_lithology();
	DROP TABLE IF EXISTS xform_gwells_well;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION gwells_full_replicate () IS 'SQL Driver script to run full replication, without code table refresh.'; 


