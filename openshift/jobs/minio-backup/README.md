# S3/minio document backup

This job connects to an s3 provider (via an OpenShift service) and makes a backup of buckets to a PVC.

rclone is used to sync between the S3 provider and the mounted PVC.
See https://rclone.org/s3/.

It then syncs the files to NFS storage using restic (see https://restic.net/)
