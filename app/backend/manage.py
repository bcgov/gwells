#!/usr/bin/env python
import os
import sys

# This is a superfluous message 

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gwells.settings")

    from django.core.management import execute_from_command_line

    from django.conf import settings

    if settings.DEBUG:
        if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
            if not os.environ.get('PYCHARM_HOSTED'):
                import ptvsd
                ptvsd.enable_attach(address = ('0.0.0.0', 3000))
                print("Attached remote debugger ptvsd")
            else:
                print("ptvsd is not compatible with PyCharm, it uses pydevd")
    execute_from_command_line(sys.argv)
