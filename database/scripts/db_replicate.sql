DROP FUNCTION IF EXISTS db_replicate_step1(boolean);

/*** NOTE: There is no refresh of the static Code Tables, as that is dependent upon, and done during 
           GWELLS Application code deployment.

		   This driver SQL script is meant to be run from the Database Pod, during scheduled nightly
		   replications or on an ad-hoc fashion. It is not part of an application deployment.

		   Therefore, there is a dependency on having all static code tables populated.

		   true : replicate just a subset of rows (analogous to $DB_REPLICATE="Subset") 
		   false: replicate all rows (analogous to $DB_REPLICATE="Full") 

	On the Postgres DB Pod:
	psql -t -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c 'SELECT db_replicate_step1(_subset_ind=>true);'

	As a remote task:
	oc exec postgresql-80-04n7h -- /bin/bash -c 'psql -t -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c "SELECT db_replicate_step1(_subset_ind=>false);"' 

    If run on local Developer workstation, ensure that you have Environment variables set
    for $POSTGRESQL_DATABASE, $POSTGRESQL_USER

 ***/
CREATE OR REPLACE FUNCTION db_replicate_step1(_subset_ind boolean default true) RETURNS void AS $$
BEGIN
	PERFORM populate_xform(_subset_ind);
	TRUNCATE TABLE bcgs_number CASCADE;	
	PERFORM migrate_bcgs();
	TRUNCATE TABLE well CASCADE;	
	PERFORM populate_well();	
	PERFORM migrate_screens();
	PERFORM migrate_production();
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION db_replicate_step1 (boolean) IS 'SQL Driver script to run replication, without code table refresh (step 1).'; 


DROP FUNCTION IF EXISTS db_replicate_step2();

/*** NOTE: This db_replicate is broken into steps, as the full all-at-once version was causing DB corruption errors ("past EOF").  
           Running as two separate psql sessions seems to help avoid this error.

		   This driver SQL script is meant to be run from the Database Pod, during scheduled nightly
		   replications or on an ad-hoc fashion. It is not part of an application deployment.

		   Therefore, there is a dependency on having all static code tables populated.

	On the Postgres DB Pod:
	psql -t -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c 'SELECT db_replicate_step2 ();'

	As a remote task:
	oc exec postgresql-80-04n7h -- /bin/bash -c 'psql -t -d $POSTGRESQL_DATABASE -U $POSTGRESQL_USER -c "SELECT db_replicate_step2 ();"' 

    If run on local Developer workstation, ensure that you have Environment variables set
    for $POSTGRESQL_DATABASE, $POSTGRESQL_USER

 ***/
CREATE OR REPLACE FUNCTION db_replicate_step2 () RETURNS void AS $$
BEGIN
	PERFORM migrate_casings();
	PERFORM migrate_perforations();
	PERFORM migrate_aquifers();
	PERFORM migrate_lithology();
	DROP TABLE IF EXISTS xform_well;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION db_replicate_step2 () IS 'SQL Driver script to run replication, without code table refresh (step 2).'; 
