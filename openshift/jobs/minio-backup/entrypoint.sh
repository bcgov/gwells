#!/bin/sh
set -e

# Check if repository is initialized.  If not, initialize it.
# RESTIC_PASSWORD is required.
if ! restic -r /backup/gwells-documents snapshots > /dev/null 2>&1; then
    restic -r /backup/gwells-documents init ; fi

# Backup files using delta (de-duplicate) and encryption
restic -r /backup/gwells-documents backup /docs

# Clean up old snapshots.
# As an example, the following arguments:
# --keep-daily 7 --keep-weekly 5 --keep-monthly 12 --keep-yearly 2
# will keep the most recent 7 daily snapshots, 5 weekly, 12 monthly, and 2 yearly snapshots.
# The rest will be pruned.
restic -r /backup/gwells-documents forget --keep-daily 7 --keep-weekly 5 --keep-monthly 12 --keep-yearly 10 --prune

# check repository integrity before exiting
restic -r /backup/gwells-documents check
