#!/bin/sh
set -e

# clone Minio data using rclone
# https://docs.min.io/docs/rclone-with-minio-server.html
# must set environment variables for remote named "minio" per https://rclone.org/docs/#config-file
rclone --size-only copy minio:aquifer-docs /backup/gwells-documents/aquifer-docs
rclone --size-only copy minio:gwells-private /backup/gwells-documents/gwells-private
rclone --size-only copy minio:gwells-private-aquifers /backup/gwells-documents/gwells-private-aquifers
rclone --size-only copy minio:gwells-private-docs /backup/gwells-documents/gwells-private-docs
rclone --size-only copy minio:gwells-private-registries /backup/gwells-documents/gwells-private-registries
rclone --size-only copy minio:submissions /backup/gwells-documents/submissions

# Check if NFS repository is initialized.  If not, initialize it.
# RESTIC_PASSWORD is required.
if ! restic -r /mnt/dest/gwells-documents snapshots > /dev/null 2>&1; then
    restic -r /mnt/dest/gwells-documents init ; fi

# Backup files using delta (de-duplicate) and encryption
restic -r /mnt/dest/gwells-documents backup /backup/gwells-documents

# Clean up old snapshots.
# As an example, the following arguments:
# --keep-daily 7 --keep-weekly 5 --keep-monthly 12 --keep-yearly 2
# will keep the most recent 7 daily snapshots, 5 weekly, 12 monthly, and 2 yearly snapshots.
# The rest will be pruned.
restic -r /mnt/dest/gwells-documents forget --keep-daily 7 --keep-weekly 5 --keep-monthly 12 --keep-yearly 10 --prune

# check repository integrity before exiting
restic -r /mnt/dest/gwells-documents check
