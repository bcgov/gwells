import os
import json
from io import open
from django.conf import settings


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

            # in dev envs, nonexistent foreign keys may prevent data import, so ignore those.
            if settings.DEBUG:
                try:
                    model.objects.create(pk=item.get('pk'), **data)
                except ValueError:
                    pass
            # in production / staging, we want to know when data is inconsistent though.
            else:
                model.objects.create(pk=item.get('pk'), **data)

    def unload_fixture(self, apps, schema_editor):
        for item in self.fixture:
            app, model = item.get('model').split('.', 1)
            model = apps.get_model(app, model)
            # The fixture in question may have been deleted for other reasons, so we don't force a
            # delete. If the record exists, then delete it.
            item = model.objects.filter(pk=item.get('pk')).first()
            if item:
                item.delete()

    def _process_fixture_file(self, fixture_path):
        with open(fixture_path, 'r') as json_data:
            data = json.load(json_data)
            for item in data:
                yield item

    def __init__(self, fixture_path):
        self.fixture = self._process_fixture_file(fixture_path)
