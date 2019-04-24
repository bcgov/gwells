#!/bin/sh
set -e

mkdir -p /backup/gwells-documents

# clone Minio data using rclone
# https://docs.min.io/docs/rclone-with-minio-server.html
# must set environment variables for remote named "minio" per https://rclone.org/docs/#config-file
for bucket in "$@"
do
    echo "rclone --size-only copy minio:$bucket /backup/gwells-documents/$bucket"
    rclone --size-only copy minio:$bucket /backup/gwells-documents/$bucket
done

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
