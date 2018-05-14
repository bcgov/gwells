# Scripts to copy Well Driller & Pump Installer data to Openshift DEV environments

## Copy from MS Access exports

All files and scripts in this xfer-registries-to-openshift are temporary until we cut over to GWELLS Registries from the MS Access system.  At that time, there will no longer be a need for replication from the legacy MS Access system, via the convoluted process of:
1. Export two CSV files from MS Access
   - well_drillers_reg.csv
   - pump_install_drillers_reg.csv
   - ignored due to data issue (Registration Action Tracking_Driller.csv, Removed From Registry.csv)
2. Obfuscate the birthday columns, in new CSV files
   - well_drillers_reg.sanitized.csv
   - pump_install_reg.sanitized.csv@
3. Store these two files in a subdirectory outside of the cloned GitHub Repo
4. Create symlinks to support local testing
   - cd ./database/codetables/registries
   - ln -s <outside of git repo> well_drillers_reg.sanitized.csv
   - ln -s <outside of git repo> pump_install_reg.sanitized.csv


Once this local setup is configured, the dev can run the scripts under 	[../../database/codetables/registries/] to load the Registries data onto their local database.

To transfer these files on the OpenShift environments, see [./setup-xfer.sh <openshift-project>].

