DROP FUNCTION IF EXISTS gwells_db_replicate(boolean);

/*** NOTE: There is no refresh of the static Code Tables, as that is dependent upon, and done during 
           GWELLS Application code deployment.

		   This driver SQL script is meant to be run from the Database Pod, during scheduled nightly
		   replications or on an ad-hoc fashion. It is not part of an application deployment.

		   Therefore, there is a dependency on having all static code tables populated.

		   true : replicate just a subset of rows (analogous to $DB_REPLICATE="Subset") 
		   false: replicate all rows (analogous to $DB_REPLICATE="Full") 
111350
12963
	On the Postgres DB Pod:
	psql -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c 'SELECT gwells_db_replicate(true);'

	As a remote task:
	oc exec postgresql-80-04n7h -- /bin/bash -c 'psql -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c "SELECT gwells_db_replicate(false);"' 

    If run on local Developer workstation, ensure that you have Environment variables set
    for $POSTGRESQL_DATABASE, $POSTGRESQL_USER

 ***/
CREATE OR REPLACE FUNCTION gwells_db_replicate(_subset_ind boolean default true) RETURNS void AS $$
BEGIN
	PERFORM gwells_populate_xform(_subset_ind);
	TRUNCATE TABLE gwells_bcgs_number CASCADE;	
	PERFORM gwells_migrate_bcgs();
	TRUNCATE TABLE gwells_well CASCADE;	
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

COMMENT ON FUNCTION gwells_db_replicate (boolean) IS 'SQL Driver script to run replication, without code table refresh.'; 

