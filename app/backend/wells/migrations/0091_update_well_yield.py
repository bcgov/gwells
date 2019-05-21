from django.db import migrations
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat


# This can be deleted when doing next squash of migrations because it's a one time update
def update_well_yield(apps, schema_editor):
    well = apps.get_model('wells', 'well')

    # update GPH well yield to USGPM
    well.objects.filter(well_yield_unit='GPH').update(
        well_yield=F('well_yield') * 0.0166667)

    # update well yield code from GPH to USGPM with internal comments
    gph = well.objects.filter(well_yield_unit='GPH')
    gph.update(internal_comments=Concat(F('internal_comments'),
                                        Value(' - Updated well_yield and well_yield_units from gph to usgpm in '
                                              'order to have standardized units and support GWELLS data '
                                              'migration May 21st 2019.'), output_field=CharField()))
    gph.update(well_yield_unit='USGPM')

    # update well yield code GPM to USGPM with internal comments
    gpm = well.objects.filter(well_yield_unit='GPM')
    gpm.update(internal_comments=Concat(F('internal_comments'),
                                        Value(" - Updated well_yield_unit_code to USGPM in order to have standardized "
                                              "units and support GWELLS data migration May 21st 2019. Records "
                                              "historically listed as GPM could have either indicated USGPM or "
                                              "Imperial GPM - please refer to original well record.",
                                              output_field=CharField())))
    gpm.update(well_yield_unit='USGPM')

    # update dummy 0 values to null
    well.objects.filter(well_yield=0).update(well_yield=None)


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0090_auto_20190521_2059'),
    ]

    operations = [
        migrations.RunPython(update_well_yield, reverse),
    ]

