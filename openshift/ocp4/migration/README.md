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
- [ ] Double check everything on Silver.
- [ ] Make sure no traffic is getting processed in Pathfinder.

### Next Steps
- [ ] Create a ticket with INFRA to change their reverse proxy for `apps.nrs.gov.bc.ca/gwells` from Pathfinder to Silver
- [ ] Remove forward proxy on Pathfinder to Silver and convert into a redirect. This will make it noticeable to anyone who uses the pathfinder URLs (APIs), and give them a chance to update their URLs.

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

### Running the database migration script
**NOTE:** You need your Pathfinder auth token and Silver auth token. Have it handy beforehand.

Inside the `migrator-cli` pod:
```/bin/bash
cd scripts

# Run the script
./migrate_database.sh
```