\echo 'Starting to clear GWELLS tables procedure...'

-- Reset tables (this truncates dependent tables too i.e. registries app)
TRUNCATE TABLE province_state_code CASCADE;

\echo 'Finished clearing GWELLS project tables.'