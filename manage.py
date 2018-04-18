#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gwells.settings")

    from django.core.management import execute_from_command_line

    is_testing = 'test' in sys.argv

    if is_testing:
        import coverage
        cov = coverage.coverage(source=['gwells', 'registries'], omit=['*/tests/*', '*/*tests.py'])
        cov.set_option('report:show_missing', True)
        cov.erase()
        cov.start()

    execute_from_command_line(sys.argv)

    if is_testing:
        cov.stop()
        cov.save()
        cov.report()
