# S3/minio document backup

This job connects to a PVC containing files to backup and makes a copy to a second PVC. It then syncs the files to NFS storage using restic (see https://restic.net/).

This leaves 3 copies of the data:  the original (in-use) PVC that is mounted by the minio service,
a backup PVC in the cluster that is only mounted by the backup job pods during backup (e.g. gwells-documents-staging-backup-vol), and the provisioned NFS storage (restic repository).


Example usage in Jenkins pipeline:

```groovy
def docBackupCronjob = openshift.process("-f",
    "openshift/jobs/minio-backup.cj.yaml",
    
    // values for the environment that this job will run in
    "NAME_SUFFIX=${prodSuffix}",
    "NAMESPACE=${prodProject}",

    // this is the backup image version created by the build config in this folder (minio-backup.bc.yaml)
    "VERSION=v1.0.0",
    "SCHEDULE='15 12 * * *'",

    // the name of the target backup PVC for the restic repository.  This will be the 3rd backup.
    // the 2nd backup will be a PVC created by the minio-backup.cj.yaml template.
    // GWELLS uses a provisioned NFS storage claim for this value.
    "DEST_PVC=${backupPVC}", 
    "SOURCE_PVC=${minioDataPVC}", // the name of the minio data PVC
    "PVC_SIZE=40Gi" // you may need enough space to hold a few copies of files on-disk.
)
```
