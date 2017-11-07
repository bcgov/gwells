/* Additional updaates to DB stucture, as Python's model.py has limited abilities to do this */
drop index if exists gwells_well_latlong cascade;
create index gwells_well_latlong on gwells_well (latitude, longitude);