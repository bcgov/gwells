import csv
import zipfile

from django.core.management.base import BaseCommand
from django.db import models

import xlsxwriter

from wells.models import Well, LithologyDescription, Casing, Screen, ProductionData, Perforation


class Command(BaseCommand):

    # def export_well(self, workbook):
    #     worksheet = workbook.add_worksheet('well')

    #     model_fields = Well._meta.get_fields()
    #     print('Fields not used in export:')
    #     for mod_field in model_fields:
    #         if mod_field.name not in WellExportSerializer.Meta.fields:
    #             print("'{}',".format(mod_field.name))

    #     # Write the headings
    #     for index, field in enumerate(WellExportSerializer.Meta.fields):
    #         worksheet.write(0, index, '{}'.format(field))

    #     # Write the values
    #     for row, well in enumerate(Well.objects.all()):
    #     # for row, well in enumerate(Well.objects.filter(well_tag_number=66449)):
    #         serializer = WellExportSerializer(well)
    #         for col, value in enumerate(serializer.data.items()):
    #             if value[1]:
    #                 worksheet.write(
    #                     row+1,
    #                     col, '{}'.format(value[1]))
    #         if row % 1000 == 0:
    #             print('row: {}'.format(row))

    def export(self, workbook, gwells_zip, worksheet_name, fields, lookup, objects):
        print('exporting: {}'.format(worksheet_name))
        worksheet = workbook.add_worksheet(worksheet_name)
        csv_file = '{}.csv'.format(worksheet_name)
        with open(csv_file, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, dialect='excel')

            values = []
            # Write the headings
            for index, field in enumerate(fields):
                worksheet.write(0, index, '{}'.format(field))
                values.append(field)
            csvwriter.writerow(values)

            # Write the values
            for row, record in enumerate(objects):
                values = []
                for col, field in enumerate(fields):
                    if field in lookup:
                        value = getattr(record, field)
                        if value:
                            value = getattr(value, lookup[field])
                    else:
                        value = getattr(record, field)
                    if value:
                        worksheet.write(
                            row+1,
                            col, '{}'.format(value))
                    values.append(value)
                csvwriter.writerow(values)
                if row % 1000 == 0:
                    print('{} row: {}'.format(worksheet_name, row))
                if row == 5000:
                    break
        gwells_zip.write(csv_file)

    # def export_ser(self, workbook, worksheet_name, serializer, objects):
    #     # Using the serializer is unfortunately just too slow
    #     worksheet = workbook.add_worksheet(worksheet_name)

    #     # Write the headings
    #     for index, field in enumerate(serializer.Meta.fields):
    #         worksheet.write(0, index, '{}'.format(field))

    #     # Write the values
    #     for row, record in enumerate(objects):
    #         serializer = serializer(record)
    #         for col, value in enumerate(serializer.data.items()):
    #             if value[1]:
    #                 worksheet.write(
    #                     row+1,
    #                     col, '{}'.format(value[1]))
    #         if row % 1000 == 0:
    #             print('row: {}'.format(row))

    def handle(self, *args, **options):
        #######
        # WELL
        #######
        well_fields = (
            # Identifiers
            'well_tag_number', 'identification_plate_number', 'well_identification_plate_attached',
            # Well Type
            'well_status', 'well_class', 'well_subclass', 'intended_water_use', 'licenced_status',
            'observation_well_number', 'observation_well_status', 'water_supply_system_name',
            'water_supply_system_well_name',
            # Location Information
            'street_address', 'city', 'legal_lot', 'legal_plan', 'legal_district_lot', 'legal_block',
            'legal_section', 'legal_township', 'legal_range', 'legal_pid', 'well_location_description',
            'latitude', 'longitude', 'utm_zone_code', 'utm_northing', 'utm_easting',
            'utm_accuracy_code', 'bcgs_id',
            # Dates
            'construction_start_date', 'construction_end_date', 'alteration_start_date',
            'alteration_end_date', 'decommission_start_date', 'decommission_end_date',
            # Who completed work
            'driller_name', 'consultant_name', 'consultant_company',
            # Well Completion
            'diameter', 'total_depth_drilled', 'finished_well_depth', 'final_casing_stick_up',
            'bedrock_depth', 'ground_elevation', 'ground_elevation_method', 'static_water_level',
            'well_yield', 'artesian_flow', 'artesian_pressure', 'well_cap_type', 'well_disinfected',
            'drilling_method', 'other_drilling_method', 'well_orientation',
            'alternative_specs_submitted',
            # Surface Seal and Backfill
            'surface_seal_material', 'surface_seal_method', 'surface_seal_length', 'backfill_type',
            'backfill_depth',
            # Liner
            'liner_material', 'liner_diameter', 'liner_thickness', 'surface_seal_thickness',
            'liner_from', 'liner_to',
            # Screen and Filter Pack
            'screen_intake_method', 'screen_type', 'screen_material', 'other_screen_material',
            'screen_opening', 'screen_bottom', 'other_screen_bottom', 'filter_pack_from',
            'filter_pack_to', 'filter_pack_material', 'filter_pack_material_size',
            # Well Developmet
            'development_hours', 'development_notes',
            # Water Quality
            # 'water_quality_characteristics', <-- bug exporting, come back to this later!
            'water_quality_colour', 'water_quality_odour', 'ems_id',
            # Decommission
            'decommission_reason', 'decommission_method', 'decommission_details', 'sealant_material',
            'backfill_material',
            # Other
            'comments', 'aquifer_id',
            # ????
            'land_district',
            'drilling_company',
            'filter_pack_thickness',
            'development_method',
            'well_yield_unit',
            'ems',
            'aquifer',
            'driller_responsible',
            )
        well_fast_lookup = {
            'well_status': 'well_status_code',
            'well_class': 'well_class_code',
            'well_subclass': 'well_subclass_code',
            'intended_water_use': 'intended_water_use_code',
            'licenced_status': 'licenced_status_code',
            'bcgs_id': 'bcgs_number',
            'land_district': 'land_district_code',
            'drilling_company': 'drilling_company_code',
            'well_yield_unit': 'well_yield_unit_code',
            # 'water_quality_characteristics': 'code'
        }
        # well_query = Well.objects.filter(well_tag_number=66449)
        well_query = Well.objects.all()\
            .order_by('well_tag_number')\
            .prefetch_related(
                'well_status',
                'well_class',
                'well_subclass',
                'intended_water_use',
                'licenced_status',
                'bcgs_id',
                'land_district',
                'drilling_company',
                'well_yield_unit'
            )
        ###########
        # LITHOLOGY
        ###########
        lithology_fields = ('well', 'lithology_from', 'lithology_to', 'lithology_raw_data',
                            'lithology_description', 'lithology_material', 'lithology_hardness',
                            'lithology_colour', 'water_bearing_estimated_flow', 'lithology_observation')
        lithology_fast_lookup = {
            'well': 'well_tag_number',
            'lithology_description': 'lithology_description_code',
            'lithology_material': 'lithology_material_code',
            'lithology_hardness': 'lithology_hardness_code',
            'lithology_colour': 'lithology_colour_code',

        }
        lithology_query = LithologyDescription.objects.filter(well__isnull=False)\
            .order_by('well__well_tag_number')\
            .prefetch_related(
                'lithology_description', 'lithology_material', 'lithology_hardness', 'lithology_colour'
            )
        ########
        # CASING
        ########
        casing_fields = ('well', 'start', 'end', 'diameter', 'casing_code', 'casing_material',
                         'wall_thickness', 'drive_shoe')
        casing_fast_lookup = {
            'well': 'well_tag_number',
            'casing_code': 'code',
            'casing_material': 'code'
        }
        casing_query = Casing.objects.filter(well__isnull=False)\
            .order_by('well__well_tag_number')\
            .prefetch_related(
                'casing_code',
                'casing_material'
            )
        ########
        # SCREEN
        ########
        screen_fields = ('well', 'start', 'end', 'internal_diameter', 'assembly_type', 'slot_size')
        screen_fast_lookup = {
            'well': 'well_tag_number',
            'assembly_type': 'screen_assembly_type_code'
        }
        screen_query = Screen.objects.filter(well__isnull=False)\
            .order_by('well__well_tag_number')\
            .prefetch_related('assembly_type')
        ############
        # PRODUCTION
        ############
        production_fields = ('well', 'yield_estimation_method', 'yield_estimation_rate',
                             'yield_estimation_duration', 'static_level', 'drawdown',
                             'hydro_fracturing_performed', 'hydro_fracturing_yield_increase')
        production_fast_lookup = {
            'yield_estimation_method': 'yield_estimation_method_code',

        }
        production_query = ProductionData.objects.filter(well__isnull=False)\
            .order_by('well__well_tag_number')\
            .prefetch_related('yield_estimation_method')
        ##############
        # PERFORATIONS
        ##############
        perforation_fields = ('well_tag_number', 'liner_thickness', 'liner_diameter', 'liner_from',
                              'liner_to', 'liner_perforation_from', 'liner_perforation_to')
        perforation_fast_lookup = {'well_tag_number': 'well_tag_number'}
        perforation_query = Perforation.objects.filter(well_tag_number__isnull=False)\
            .order_by('well_tag_number__well_tag_number')
        
        # ### I wonder? We could possibly get things to be a lot faster using raw sql?
        # from django.db import connection
        # # If using cursor without "with" -- it must be closed explicitly:
        # with connection.cursor() as cursor:
        #     cursor.execute('select column1, column2, column3 from table where aaa=%s', [5])
        #     for row in cursor.fetchall():
        #         print row[0], row[1], row[3]

        with zipfile.ZipFile('gwells.zip', 'w') as gwells_zip:
            with xlsxwriter.Workbook('hello.xlsx') as workbook:
                self.export(workbook, gwells_zip, 'well', well_fields, well_fast_lookup, well_query)
                self.export(workbook, gwells_zip, 'lithology', lithology_fields, lithology_fast_lookup,
                            lithology_query)
                self.export(workbook, gwells_zip, 'casing', casing_fields, casing_fast_lookup, casing_query)
                self.export(workbook, gwells_zip, 'screen', screen_fields, screen_fast_lookup, screen_query)
                self.export(workbook, gwells_zip, 'production', production_fields, production_fast_lookup,
                            production_query)
                self.export(workbook, gwells_zip, 'perforation', perforation_fields, perforation_fast_lookup,
                            perforation_query)
        print('done')
