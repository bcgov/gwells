DROP FUNCTION IF EXISTS migrate_bcgs();

CREATE OR REPLACE FUNCTION migrate_bcgs() RETURNS void AS $$
DECLARE
  row_count integer;
BEGIN
	raise notice '...importing wells_screens data';

	INSERT INTO bcgs_number (
	 create_user, create_date, update_user, update_date, bcgs_id, bcgs_number
	)
	SELECT
	 who_created ,when_created ,who_updated ,when_updated, bcgs_id, bcgs_number
	FROM WELLS.WELLS_BCGS_NUMBERS
	ORDER BY BCGS_NUMBER;

	raise notice '...BCGS data imported into the bcgs_number table';
	SELECT count(*) from bcgs_number into row_count;
	raise notice '% rows loaded into the bcgs_number table',  row_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION migrate_bcgs () IS 'Load BCGS numbers from legacy Oracle Database using Foreign Data Wrapper.'; 

