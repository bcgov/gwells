#!/bin/sh


# Halt on errors/unsets, change fail returns, change field separator, verbose mode
#
set -euo pipefail
IFS=$'\n\t'
[ "${VERBOSE:-}" != true ]|| set -x


# PVC mount and folder variables, removing any trailing slashes (%/)
#
SRC_MNT=${SRC_MNT:-/mnt/src}
DEST_MNT=${DEST_MNT:-/mnt/dest}
SRC_MNT=${SRC_MNT%/}
DEST_MNT=${DEST_MNT%/}
#
DEST_DIR=${DEST_MNT}/$(hostname)
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
