DROP FUNCTION IF EXISTS gwells_migrate_bcgs();

CREATE OR REPLACE FUNCTION gwells_migrate_bcgs() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
	raise notice '...importing wells_screens data';

	INSERT INTO gwells_bcgs_number (
	 create_user 
	,create_date
	,update_user 
	,update_date
	,bcgs_id     
	,bcgs_number 
	)
	SELECT
	 who_created
	,when_created
	,who_updated
	,when_updated
	,bcgs_id      
	,bcgs_number 
	FROM WELLS.WELLS_BCGS_NUMBERS
	ORDER BY BCGS_NUMBER;

	raise notice '...BCGS data imported into the gwells_bcgs_number table';
	SELECT count(*) from gwells_bcgs_number into row_count;
	raise notice '% rows loaded into the gwells_bcgs_number table',  row_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION gwells_migrate_bcgs () IS 'Load BCGS numbers from legacy Oracle Database using Foreign Data Wrapper.'; 

