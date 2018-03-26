# Scripts to copy Well Driller & Pump Installer data to Openshift DEV environments

## Copy from MS Access exports

All files and scripts in this xfer-registries-to-openshift are temporary until we cut over to GWELLS Registries from the MS Access system.  At that time, there will no longer be a need for replication from the legacy MS Access system, via the convoluted process of:
1. Export three CSV files from MS Access
   - Registration Action Tracking_Driller.csv
   - Removed From Registry.csv
   - well_drillers_reg.csv
2. Obfuscate the birthday columns, in new CSV files
   - Registration Action Tracking_Driller.sanitized.csv
   - Removed From Registry.sanitized.csv
   - well_drillers_reg.sanitized.csv
3. Store these three files in a subdirectory outside of the cloned GitHub Repo
4. Create symlinks to support local testing
   - cd ./database/code-tables/registries
   - ln -s <outside of git repo> well_drillers_reg.sanitized.csv
   - ln -s <outside of git repo> "Removed From Registry.sanitized.csv"
   - ln -s <outside of git repo> "Registration Action Tracking_Driller.sanitized.csv"

Once this local setup is configured, the dev can run the scripts under 	./database/code-tables/registries/ to load the Registries data onto their local database.

To transfer these files on the OpenShift environments, see setup-xfer.sh.