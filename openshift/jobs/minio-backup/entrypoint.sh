#!/bin/sh
set -euo pipefail
IFS=$'\n\t'
[ "${VERBOSE:-}" != true ]|| set -x

# PVC mount and folder variables, removing any trailing slashes (%/)
#
SRC_MNT=${SRC_MNT:-/mnt/source}
DEST_MNT=${DEST_MNT:-/backup}
SRC_MNT=${SRC_MNT%/}
DEST_MNT=${DEST_MNT%/}
#
DEST_DIR=${DEST_MNT}/documents
TMP_BK=${NEW_BK:-${DEST_DIR}/bk-tmp}
PRV_BK=${PRV_BK:-${DEST_DIR}/bk-prev}
NEW_BK=${NEW_BK:-${DEST_DIR}/bk}


# Drop to one previous backup
# Either directory does not exist, or remove directory.
[ ! -d ${PRV_BK} ]|| rm -rf ${PRV_BK}


# Copy and verify
#
mkdir -p ${TMP_BK}
if ! rsync -avh ${SRC_MNT}/ ${TMP_BK}/
then
	echo "Copy failed!  Previous backups retained."
	rm -rf ${TMP_BK}
	exit 1
fi


# Shuffle and show disk usage
# Either directory doesn't exist, or move it
[ ! -d ${NEW_BK} ]|| mv ${NEW_BK} ${PRV_BK}
mv ${TMP_BK} ${NEW_BK}
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
