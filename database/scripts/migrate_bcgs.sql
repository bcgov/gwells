\echo '...importing wells_screens data'
INSERT INTO gwells_bcgs_number (
 who_created 
,when_created
,who_updated 
,when_updated
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

\echo 'BCGS data imported into the gwells_bcgs_number table';

\t
SELECT count(*) || ' rows loaded into the gwells_bcgs_number table' FROM gwells_bcgs_number;
\t


