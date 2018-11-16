from django.core.management.base import BaseCommand

import xlsxwriter

from wells.models import Well
from wells.serializers import WellExportSerializer


class Command(BaseCommand):

    def handle(self, *args, **options):

        with xlsxwriter.Workbook('hello.xlsx') as workbook:
            worksheet = workbook.add_worksheet('well')

            model_fields = Well._meta.get_fields()
            print('Fields not used in export:')
            for mod_field in model_fields:
                if mod_field.name not in WellExportSerializer.Meta.fields:
                    print("'{}',".format(mod_field.name))

            # Write the headings
            for index, field in enumerate(WellExportSerializer.Meta.fields):
                worksheet.write(0, index, '{}'.format(field))

            # Write the values
            for well_row, well in enumerate(Well.objects.all()):
            # for row, well in enumerate(Well.objects.filter(well_tag_number=66449)):
                serializer = WellExportSerializer(well)
                for col, value in enumerate(serializer.data.items()):
                    if value[1]:
                        worksheet.write(
                            row+1,
                            col, '{}'.format(value[1]))
                if row % 1000 == 0:
                    print('row: {}'.format(row))
        print('done')
