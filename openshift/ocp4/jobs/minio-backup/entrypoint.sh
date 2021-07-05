#!/bin/sh
set -euo pipefail
IFS=$'\n\t'
[ "${VERBOSE:-}" != true ]|| set -x

# PVC mount and folder variables, removing any trailing slashes (%/)
#
DEST_MNT=${DEST_MNT:-/backup}
DEST_MNT=${DEST_MNT%/}
#
DEST_DIR=${DEST_MNT}/documents
TMP_BK=${NEW_BK:-${DEST_DIR}/bk-tmp}
NEW_BK=${NEW_BK:-${DEST_DIR}/bk}

du -hd 1 ${DEST_MNT}

# Check if NFS repository is initialized.  If not, initialize it.
# RESTIC_PASSWORD is required.
if ! restic -r /mnt/dest/gwells-documents snapshots > /dev/null 2>&1; then
    restic -r /mnt/dest/gwells-documents init ; fi

# Backup files using delta (de-duplicate) and encryption
restic --cache-dir ${DEST_DIR}/.cache -r /mnt/dest/gwells-documents backup ${NEW_BK}

# Clean up old snapshots.
# As an example, the following arguments:
# --keep-daily 7 --keep-weekly 5 --keep-monthly 12 --keep-yearly 2
# will keep the most recent 7 daily snapshots, 5 weekly, 12 monthly, and 2 yearly snapshots.
# The rest will be pruned.
restic -r /mnt/dest/gwells-documents forget --keep-daily 7 --keep-weekly 5 --keep-monthly 12 --keep-yearly 10 --prune

# check repository integrity before exiting
restic -r /mnt/dest/gwells-documents check
