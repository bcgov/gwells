DROP FUNCTION IF EXISTS create_xform_well_well_ETL_table();

CREATE OR REPLACE FUNCTION create_xform_well_well_ETL_table() RETURNS void AS $$
BEGIN

raise notice 'Starting clear_tables() procedure...';
raise notice '...creating xform_gwells_well ETL table';

DROP TABLE IF EXISTS xform_gwells_well;
CREATE unlogged TABLE IF NOT EXISTS xform_gwells_well (
   well_tag_number                integer,
   well_guid                      uuid,
   acceptance_status_code         character varying(10),
   owner_full_name                character varying(200),
   owner_mailing_address          character varying(100),
   owner_city                     character varying(100),
   owner_postal_code              character varying(10),
   street_address                 character varying(100),
   city                           character varying(50),
   legal_lot                      character varying(10),
   legal_plan                     character varying(20),
   legal_district_lot             character varying(20),
   legal_block                    character varying(10),
   legal_section                  character varying(10),
   legal_township                 character varying(20),
   legal_range                    character varying(10),
   legal_pid                      integer,
   well_location_description      character varying(500),
   identification_plate_number    integer,
   diameter                       character varying(9),
   total_depth_drilled            numeric(7,2),
   finished_well_depth            numeric(7,2),
   well_yield                     numeric(8,3),
   WELL_USE_CODE                  character varying(10),
   LEGAL_LAND_DISTRICT_CODE       character varying(10),
   province_state_guid            uuid,
   CLASS_OF_WELL_CODCLASSIFIED_BY character varying(10),
   SUBCLASS_OF_WELL_CLASSIFIED_BY character varying(10),
   well_yield_unit_guid           uuid,
   latitude                       numeric(8,6),
   longitude                      numeric(9,6),
   ground_elevation               numeric(10,2),
   well_orientation               boolean,
   other_drilling_method          character varying(50),
   drilling_method_guid           uuid,
   ground_elevation_method_guid   uuid,
   BKFILL_ABOVE_SRFC_SEAL_DEPTH   numeric(7,2), -- backfill_above_surface_seal_depth
   backfill_above_surface_seal    character varying(250),
   SEALANT_MATERIAL               character varying(100),
   status_of_well_code 	          character varying(10),
   observation_well_number	      integer,
   ministry_observation_well_stat character varying(25),
   well_licence_general_status    character varying(20),
   alternative_specifications_ind boolean,
   construction_start_date        timestamp with time zone,
   construction_end_date          timestamp with time zone,
   alteration_start_date          timestamp with time zone,
   alteration_end_date            timestamp with time zone,
   decommission_start_date        timestamp with time zone,
   decommission_end_date          timestamp with time zone,
   drilling_company_guid          uuid,
   when_created                   timestamp with time zone,
   when_updated                   timestamp with time zone,
   who_created                    character varying(30),
   who_updated                    character varying(30)
);

raise notice 'Finished create_xform_well_well_ETL_table() procedure.';
END;
$$ LANGUAGE plpgsql;
