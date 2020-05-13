import json
from decimal import Decimal


class GeoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class GeoJSONIterator():

    def __init__(self, queryset_iter, compute_bbox=False, geometry_col_name='geom'):
        self.send_header = True
        self.done = False
        self.first_record = True
        self.has_records = False
        self.geometry_col_name = geometry_col_name
        self.compute_bbox = compute_bbox

        self.iterator = queryset_iter
        self.extent = [float('inf'), float('inf'), float('-inf'), float('-inf')]

    def get_header(self):
        return '{"type": "FeatureCollection","features": ['

    def get_footer(self):
        bbox = ''
        # we have computed the bbox and there is at least one record
        if self.compute_bbox and self.has_records:
            bbox = ',\n"bbox": ' + str(self.extent)

        return ']' + bbox + "}"

    def json_dumps_record(self, record):
        """ JSON encodes a feature """

        geometry = record.pop(self.geometry_col_name)

        self.has_records = True

        is_point = geometry.geom_typeid == 0

        point_lng = None
        point_lat = None
        if is_point:
            (point_lng, point_lat) = geometry.coords

        if self.compute_bbox:
            if is_point:
                (xmin, ymin, xmax, ymax) = (point_lng, point_lat, point_lng, point_lat)
            else:
                (xmin, ymin, xmax, ymax) = geometry.extent
            if xmin < self.extent[0]:
                self.extent[0] = xmin
            if ymin < self.extent[1]:
                self.extent[1] = ymin
            if xmax > self.extent[2]:
                self.extent[2] = xmax
            if ymax > self.extent[3]:
                self.extent[3] = ymax

        properties = json.dumps(record, cls=GeoJSONEncoder)

        # The GEOSGeometry `.json` is slow for Points. Build the geometry JSON manually instead
        geometry_json = ''
        if is_point:
            geometry_json = '{"type": "Point", "coordinates": [%.5f,%.5f]}' % (point_lng, point_lat)
        else:
            geometry_json = geometry.json

        return '{"type": "Feature", "geometry": ' + geometry_json + \
            ', "properties": ' + properties + '}'

    def __iter__(self):
        return self

    def __next__(self):
        if self.send_header:
            # If we're right at the start, send the header.
            self.send_header = False
            return self.get_header()
        elif self.done:
            # If we're done, be done!
            raise StopIteration

        # If we're chugging along, send a record.
        try:
            record = next(self.iterator)
            record = self.json_dumps_record(record)
            comma = ','
            if self.first_record:
                self.first_record = False
                comma = ''
            return f"{comma}\n{record}"
        except StopIteration:
            # No more records? Send the footer.
            self.done = True
            return self.get_footer()
