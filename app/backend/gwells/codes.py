import os
import json
from io import open


class CodeFixture():
    """Loads JSON code table fixtures into database using migrations.
    Usage:
        from gwells.codes import CodeFixture
        fixtures = CodeFixture('codes.json')
        fixtures.load_fixture()

        # remove fixtures (for rolling back migrations)
        fixtures.unload_fixture()
    """

    def load_fixture(self, apps, schema_editor):
        for item in self.fixture:
            data = item.get('fields')

            # determine app and model that the item belongs to
            app, model = item.get('model').split('.', 1)
            model = apps.get_model(app, model)

            model.objects.create(pk=item.get('pk'), **data)

    def unload_fixture(self, apps, schema_editor):
        for item in self.fixture:
            app, model = item.get('model').split('.', 1)
            model = apps.get_model(app, model)
            model.objects.get(pk=item.get('pk')).delete()

    def _process_fixture_file(self, fixture_path):
        with open(fixture_path, 'r') as json_data:
            data = json.load(json_data)
            for item in data:
                yield item

    def __init__(self, fixture_path):
        self.fixture = self._process_fixture_file(fixture_path)
