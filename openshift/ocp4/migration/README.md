# Migration
 
## Migration steps
Here are the steps we need to do to migrate from the Openshift Container Platform (OCP) version 3 to version 4. 
To avoid confusion, let's call OCP3 Pathfinder and OCP4 Silver.

### Before you start
You need:
- [ ] Migrator CLI Deployment Config
   - Used to migrate the database (gwells and tileserver views)
- [ ] Minio mirror `mc mirror` setup from Silver to Pathfinder

### Migration checklist 
- [ ] Make sure all services are down to prevent users from entering data and uploading documents
- [ ] Migrate database
- [ ] Turn off `mc mirror` on OCP3 and make sure the settings for minio on Silver work
- [ ] Make sure the settings for AWS (public documents) on Silver are working
- [ ] Change or copy `gwells-maintenance` reverse proxy config to gwells on Pathfinder
- [ ] Double check everything on Silver.
- [ ] Make sure no traffic is getting processed in Pathfinder.

### Next Steps
- [ ] Create a ticket with NRS to change their reverse proxy for `apps.nrs.gov.bc.ca/gwells` from Pathfinder to Silver
- [ ] Remove forward proxy on Pathfinder to Silver and convert into a redirect. This will make it noticeable to anyone who uses the pathfinder URLs (APIs), and give them a chance to update their URLs.

## Migration tools
**migrator-cli (importer.dc.yaml)**
```bash
# Deploy migrator dc with oc cli
NAMESPACE4="26e83e-dev"
oc process -f importer.dc.yaml -p NAMESPACE=$NAMESPACE4 | oc apply -f -
```

```bash
oc -n $NAMESPACE4 create configmap migration-scripts \
--from-file=scripts/
```