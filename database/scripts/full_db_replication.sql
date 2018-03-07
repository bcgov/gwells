DROP FUNCTION IF EXISTS full_replicate();

/*** NOTE: There is no refresh of Code Tables, as that is done during GWELLS Application code deployment
		   This driver SQL script is meant to be run from the Database Pod, during nightly replications,
		   not as part of an application deployment.

		   Therefore, there is a dependency on having all code tables populated, including BCGS numbers.

	On the Postgres DB Pod:
	psql -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c 'SELECT full_replicate();'

	As a remote task:
	oc exec postgresql-80-04n7h -- /bin/bash -c 'psql -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c "SELECT full_replicate();"' 



 ***/
CREATE OR REPLACE FUNCTION full_replicate() RETURNS void AS $$
BEGIN
	TRUNCATE TABLE well CASCADE;
	PERFORM populate_xform(false);
	PERFORM populate_well();	
	PERFORM migrate_screens();
	PERFORM migrate_production();
	PERFORM migrate_casings();
	PERFORM migrate_perforations();
	PERFORM migrate_aquifers();
	PERFORM migrate_lithology();
	DROP TABLE IF EXISTS xform_well;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION full_replicate () IS 'SQL Driver script to run full replication, without code table refresh.'; 


