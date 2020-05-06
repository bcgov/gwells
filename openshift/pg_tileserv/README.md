# pg_tileserv

GWELLS uses pg_tileserv to render vector tiles for displaying aquifers and wells (currently only for Aquifer search and details pages, not for all GWELLS pages).

https://github.com/CrunchyData/pg_tileserv

## Prerequisites

The pg_tileserv config in pg_tileserv.dc.yaml requires a read only database user. This user should have limited access only to data that can be rendered on the map. In GWELLS, the read only user only has usage and select privileges in the `postgis_ftw` schema, where views can be created to be made available as vector layers. For more info, see openshift/database.deploy.yml and the GWELLS Django migrations where views are created.

### nginx (basic tile cache)

nginx has been deployed as a basic tile cache. To build the nginx server and include the nginx.conf file located in this folder, run (from the GWELLS tools namespace):

`oc new-build nginx:1.12~https://github.com/bcgov/gwells.git --context-dir=openshift/pg_tileserv --name=nginx-tilecache`

The template `pg_tileserv.dc.yaml` will now be able to pull the nginx-tilecache container image. This image should be rebuilt when edits are made to the nginx.conf file. 
