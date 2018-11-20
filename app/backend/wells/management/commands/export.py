import csv
import zipfile
import os

from django.core.management.base import BaseCommand
from django.db import models
from django.db import connection

import xlsxwriter

from wells.models import Well, LithologyDescription, Casing, Screen, ProductionData, Perforation


class Command(BaseCommand):

    def export(self, workbook, gwells_zip, worksheet_name, cursor):
        # worksheet = workbook.add_worksheet(worksheet_name)
        csv_file = '{}.csv'.format(worksheet_name)
        if os.path.exists(csv_file):
            os.remove(csv_file)
        with open(csv_file, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, dialect='excel')

            values = []
            # Write the headings
            for index, field in enumerate(cursor.description):
                # worksheet.write(0, index, '{}'.format(field.name))
                values.append(field.name)
            csvwriter.writerow(values)

            # Write the values
            row_index = 0
            for row, record in enumerate(cursor.fetchall()):
                values = []
                num_values = 0
                for col, value in enumerate(record):
                    if value:
                        num_values += 1
                    values.append(value)
                if num_values > 1:
                    # We always have a well_tag_number, but if that's all we have, then just skip this record
                    row_index += 1
                    # for col, value in enumerate(values):
                    #     if value:
                    #         worksheet.write(row_index, col, value)
                    csvwriter.writerow(values)
        gwells_zip.write(csv_file)

    def handle(self, *args, **options):
        #######
        # WELL
        #######
        well_sql = ("""select well_tag_number, identification_plate_number,
 well_identification_plate_attached,
 well_status_code, well.well_class_code,
 wsc.well_class_code as well_subclass,
 intended_water_use_code, licenced_status_code,
 observation_well_number, obs_well_status_code, water_supply_system_name,
 water_supply_system_well_name,
 street_address, city, legal_lot, legal_plan, legal_district_lot, legal_block,
 legal_section, legal_township, legal_range,
 land_district_code,
 legal_pid,
 well_location_description,
 latitude, longitude, utm_zone_code, utm_northing, utm_easting,
 utm_accuracy_code, bcgs_id,
 construction_start_date, construction_end_date, alteration_start_date,
 alteration_end_date, decommission_start_date, decommission_end_date,
 driller_name, consultant_name, consultant_company,
 diameter, total_depth_drilled, finished_well_depth, final_casing_stick_up,
 bedrock_depth, ground_elevation, ground_elevation_method_code, static_water_level,
 well_yield,
 well_yield_unit_code,
 artesian_flow, artesian_pressure, well_cap_type, well_disinfected,
 drilling_method_code, other_drilling_method, well_orientation,
 alternative_specs_submitted,
 surface_seal_material_code, surface_seal_method_code, surface_seal_length,
 backfill_type,
 backfill_depth,
 liner_material_code, liner_diameter, liner_thickness, surface_seal_thickness,
 liner_from, liner_to,
 screen_intake_method_code, screen_type_code, screen_material_code,
 other_screen_material,
 screen_opening_code, screen_bottom_code, other_screen_bottom, development_method_code,
 filter_pack_from,
 filter_pack_to, filter_pack_material_code,
 filter_pack_thickness,
 filter_pack_material_size_code,
 development_hours, development_notes,
 water_quality_colour, water_quality_odour, ems_id,
 decommission_reason, decommission_method_code, decommission_details, sealant_material,
 backfill_material,
 comments, aquifer_id,
 drilling_company.drilling_company_code,
 ems,
 aquifer_id,
 registries_person.surname as driller_responsible
 from well
 left join well_subclass_code as wsc on wsc.well_subclass_guid = well.well_subclass_guid
 left join drilling_company on
 drilling_company.drilling_company_guid = well.drilling_company_guid
 left join registries_person on
 registries_person.person_guid = well.driller_responsible_guid
 order by well_tag_number""")
        ###########
        # LITHOLOGY
        ###########
        lithology_sql = ("""select well_tag_number, lithology_from, lithology_to, lithology_raw_data,
 ldc.description as lithology_description_code,
 lmc.description as lithology_material_code,
 lhc.description as lithology_hardness_code,
 lcc.description as lithology_colour_code,
 water_bearing_estimated_flow,
 well_yield_unit_code, lithology_observation
 from lithology_description
 left join lithology_description_code as ldc on
 ldc.lithology_description_code = lithology_description.lithology_description_code
 left join lithology_material_code as lmc on
 lmc.lithology_material_code = lithology_description.lithology_material_code
 left join lithology_hardness_code as lhc on
 lhc.lithology_hardness_code = lithology_description.lithology_hardness_code
 left join lithology_colour_code as lcc on
 lcc.lithology_colour_code = lithology_description.lithology_colour_code
 order by well_tag_number""")
        ########
        # CASING
        ########
        casing_sql = ("""select well_tag_number, casing_from, casing_to, diameter, casing_code,
 casing_material_code, wall_thickness, drive_shoe from casing
 order by well_tag_number""")
        ########
        # SCREEN
        ########
        screen_sql = ("""select well_tag_number, screen_from, screen_to, internal_diameter,
 screen_assembly_type_code, slot_size from screen
 order by well_tag_number""")
        ############
        # PRODUCTION
        ############
        production_sql = ("""select well_tag_number, yield_estimation_method_code, well_yield_unit_code,
 yield_estimation_rate,
 yield_estimation_duration, static_level, drawdown,
 hydro_fracturing_performed, hydro_fracturing_yield_increase from production_data
 order by well_tag_number""")
        ##############
        # PERFORATIONS
        ##############
        perforation_sql = ("""select well_tag_number, liner_from, liner_to, liner_diameter,
 liner_perforation_from, liner_perforation_to, liner_thickness
 from
 perforation
 order by well_tag_number""")

        zip_filename = 'gwells.zip'
        if os.path.exists(zip_filename):
            os.remove(zip_filename)
        with zipfile.ZipFile(zip_filename, 'w') as gwells_zip:
            spreadsheet_filename = 'gwells.xlsx'
            if os.path.exists(spreadsheet_filename):
                os.remove(spreadsheet_filename)
            workbook = None
            # with xlsxwriter.Workbook(spreadsheet_filename) as workbook:
            # Well
            with connection.cursor() as cursor:
                cursor.execute(well_sql)
                self.export(workbook, gwells_zip, 'well', cursor)
            # Lithology
            with connection.cursor() as cursor:
                cursor.execute(lithology_sql)
                self.export(workbook, gwells_zip, 'lithology', cursor)
            # Casing
            with connection.cursor() as cursor:
                cursor.execute(casing_sql)
                self.export(workbook, gwells_zip, 'casing', cursor)
            # Screen
            with connection.cursor() as cursor:
                cursor.execute(screen_sql)
                self.export(workbook, gwells_zip, 'screen', cursor)
            # Production
            with connection.cursor() as cursor:
                cursor.execute(production_sql)
                self.export(workbook, gwells_zip, 'production', cursor)
            # Perforation
            with connection.cursor() as cursor:
                cursor.execute(perforation_sql)
                self.export(workbook, gwells_zip, 'perforation', cursor)
