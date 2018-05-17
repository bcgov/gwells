import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Creates a set of groups for GWELLS users'

    def handle(self, *args, **options):
        group_gwells_admin = Group.objects.get_or_create(name="gwells_administrator")
        group_registries_stat_authority = Group.objects.get_or_create(name="registries_statutory_authority")
        group_registries_adjudicator = Group.objects.get_or_create(name="registries_adjudicator")
        group_registries_staff_viewer = Group.objects.get_or_create(name="registries_staff_viewer")

        self.stdout.write(
            self.style.SUCCESS(
                'Group %s %s' % (
                    group_gwells_admin[0].name,
                    'created' if group_gwells_admin[1] else 'exists'
                )
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                'Group %s %s' % (
                    group_registries_stat_authority[0].name,
                    'created' if group_registries_stat_authority[1] else 'exists'
                )
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                'Group %s %s' % (
                    group_registries_adjudicator[0].name,
                    'created' if group_registries_adjudicator[1] else 'exists'
                )
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                'Group %s %s' % (
                    group_registries_staff_viewer[0].name,
                    'created' if group_registries_staff_viewer[1] else 'exists'
                )
            )
        )
