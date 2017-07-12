/* Additional updaates to DB stucture, as Python's model.py has limited abilities to do this */
create index gwells_well_latlong on gwells_well (latitude, longitude);