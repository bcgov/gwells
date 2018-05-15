\echo 'Starting to clear GWELLS tables procedure...'

-- Reset tables (this truncates dependent tables too i.e. registries app)
-- TRUNCATE TABLE province_state_code CASCADE;

\echo 'Skipping clearing GWELLS project table province_state_code, as this will reset Registries tables.'