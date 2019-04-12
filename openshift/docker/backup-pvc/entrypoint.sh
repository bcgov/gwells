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
TEMP_DIR=${DEST_DIR:-${DEST_MNT}/tmp}
PREV_DIR=${PREV_DIR:-${DEST_MNT}/bk-prev}
DEST_DIR=${DEST_DIR:-${DEST_MNT}/bk}


# Drop to one previous backup
#
[ ! -d ${PREV_DIR} ]|| rm -rf ${PREV_DIR}


# Copy and verify
#
if ! rsync -avh ${SRC_MNT}/ ${TEMP_DIR}/
then
	echo "Copy failed!  Previous backups retained."
	exit 1
fi


# Shuffle and show disk usage
#
[ ! -d ${DEST_DIR} ]|| mv ${DEST_DIR} ${PREV_DIR}
mv ${TEMP_DIR} ${DEST_DIR}
du -hd 1 ${DEST_MNT}