/* Additional updaates to DB stucture, as Python's model.py has limited abilities to do this */
create index well_latlong on well (latitude, longitude);