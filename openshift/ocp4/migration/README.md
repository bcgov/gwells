# Migration
 
## Migration steps
Here are the steps we need to do to migrate from the Openshift Container Platform (OCP) version 3 to version 4. 
To avoid confusion, let's call OCP3 Pathfinder and OCP4 Silver.

### Before you start
You need:
- [ ] Migrator CLI Deployment Config
   - Used to migrate the database (gwells and tileserver views)
- [ ] Minio mirror `mc mirror` setup from Silver to Pathfinder
   - Make sure we have enough storage in Silver, and turn on `mc mirror` to rsync/mirror the files continuously until migration day

### Migration checklist 
- [ ] Make sure all services are down to prevent users from entering data and uploading documents
- [ ] [Migrate database](#running-the-database-migration-script)
- [ ] Turn off `mc mirror` on Pathfinder and make sure the settings for minio on Silver work
- [ ] Make sure the settings for AWS (public documents) on Silver are working
- [ ] Change or copy `gwells-maintenance` reverse proxy config to gwells on Pathfinder
- [ ] Stop all scheduled jobs on pathfinder
- [ ] Activate minio backups 
- [ ] Double check everything on Silver.
- [ ] Make sure no traffic is getting processed in Pathfinder.

### Next Steps
- [ ] Create a ticket with INFRA to change their reverse proxy for `apps.nrs.gov.bc.ca/gwells` from Pathfinder to Silver
- [ ] Remove reverse proxy on Pathfinder to Silver and convert into a redirect. This will make it noticeable to anyone who uses the pathfinder URLs (APIs), and give them a chance to update their URLs.

## Migration tools

### Setting up the Migrator CLI with the database migration scripts
**Migration scripts**
```bash
# Set namespace (will be used in the next script)
NAMESPACE4="26e83e-dev"

# Create a config map from the migration scripts
oc -n $NAMESPACE4 create configmap migration-scripts \
--from-file=scripts/
```

**migrator-cli (importer.dc.yaml)**
```bash
# Deploy migrator dc with oc cli
oc process -f importer.dc.yaml -p NAMESPACE=$NAMESPACE4 | oc apply -f -
```

### Running the migration script
**NOTE:** You need your Pathfinder auth token and Silver auth token. Have it handy beforehand.

Inside the `migrator-cli` pod:
```/bin/bash
cd scripts

# Run the script
# This script does all the migration steps. 
# If it fails, you may run one of the smaller migration scripts it calls and continue from there.
# It doesn't accept environment as a first param; instead it asks for it
./do_migration.sh |& tee /tmp/migration.log
```

#### Smaller migration scripts
**`migrate_database.sh`**
```bash
# This simply calls the two db migration scripts
#   db_dump_and_copy.sh and db_copy_and_restore.sh
# It doesn't accept environment as a first param; instead it asks for it
./migrate_database.sh
```

**`db_dump_and_copy.sh`**
```bash
# Run `pg_dump` (custom postgres format) on Silver, and copy the file on this volume
./db_dump_and_copy.sh [test/prod]
```

**`db_copy_and_restore.sh`**
```bash
# Copy the dump file from this volume onto the postgres pod volume
# Run `pg_restore` on postgres pod
./db_copy_and_restore.sh [test/prod]
```

**`migrate_minio.sh`**
```bash
# Run `mc mirror` on Pathfinder to copy all the buckets and files/objects to Silver.
# Also runs an `mc diff` to check if there are discrepancies
./migrate_minio.sh [test/prod]
```

**`activate_proxy.sh`**
```bash
# Switch the `gwells-staging` routes on Pathfinder to proxy pass to Silver 
./activate_proxy.sh [test/prod]

# To switch them back, add `--revert` at the end
./activate_proxy.sh [test/prod] --revert
```

**`scale_down.sh`**
```bash
# Scales down the `gwells-staging` application on Silver 
./activate_proxy.sh [test/prod]

# To scale it up, add `--revert` at the end
./activate_proxy.sh [test/prod] --revert
```

**`scale_up.sh`**
```bash
# Scales up the `gwells-staging` application on Silver 
./activate_proxy.sh [test/prod]

# To scale it up, add `--revert` at the end
./activate_proxy.sh [test/prod] --revert
```

#### Issues, tips and tricks
**Login to the migrator-cli pod terminal quickly**
I use a helper script named `rsh_migrator_cli.sh`

```bash
# Make it executable
chmod +x rsh_migrator_cli.sh 
```

```bash
# RSH into migrator-cli pod, first param is your namespace
./rsh_migrator_cli.sh 26e83e-test
```

**If you run into authorization issues while running one of the smaller migration scripts**  q
```bash
# Sample unauthorized message
error: You must be logged in to the server (Unauthorized)
```
Just delete the kubeconfig files `/tmp/KUBECONFIG` and `/tmp/KUBECONFIGSILVER`

**Minio issues**  
```bash
mc: <ERROR> Unable to create bucket at `silver/.minio.sys`. Bucket name contains invalid characters
```

You may have to move the .minio.sys folder that's in `/opt/minio/s3/data/.minio.sys`. This is just metadata so you can also delete it.
The script *does* check for this file and moves it, so you may not encounter this issue.