# S3/minio document backup

This job connects to a PVC containing files to backup and makes a copy to a second PVC. It then syncs the files to NFS storage using restic (see https://restic.net/).

This leaves 3 copies of the data:  the original (in-use) PVC that is mounted by the minio service,
a backup PVC in the cluster that is only mounted by the backup job pods during backup (e.g. gwells-documents-staging-backup-vol), and the provisioned NFS storage (restic repository).
