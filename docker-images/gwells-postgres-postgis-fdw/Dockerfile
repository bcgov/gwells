FROM rhel7

# PostgreSQL image for OpenShift.
# Volumes:
#  * /var/lib/psql/data   - Database cluster for PostgreSQL
# Environment:
#  * $POSTGRESQL_USER     - Database user name
#  * $POSTGRESQL_PASSWORD - User's password
#  * $POSTGRESQL_DATABASE - Name of the database to create
#  * $POSTGRESQL_ADMIN_PASSWORD (Optional) - Password for the 'postgres'
#                           PostgreSQL administrative account

USER 0

ENV POSTGRESQL_VERSION=9.6 \
    POSTGRESQL_PREV_VERSION=9.5 \
    HOME=/var/lib/pgsql \
    PGUSER=postgres

ENV SUMMARY="PostgreSQL is an advanced Object-Relational database management system" \
    DESCRIPTION="PostgreSQL is an advanced Object-Relational database management system (DBMS). \
The image contains the client and server programs that you'll need to \
create, run, maintain and access a PostgreSQL DBMS server."

LABEL summary=$SUMMARY \
      description="$DESCRIPTION" \
      io.k8s.description="$DESCRIPTION" \
      io.k8s.display-name="PostgreSQL 9.6" \
      io.openshift.expose-services="5432:postgresql" \
      io.openshift.tags="database,postgresql,postgresql96,rh-postgresql96" \
      name="rhscl/postgresql-96-rhel7" \
      com.redhat.component="rh-postgresql96-docker" \
      version="9.6" \
      release="1"

EXPOSE 5432

COPY root/usr/libexec/fix-permissions /usr/libexec/fix-permissions

# This image must forever use UID 26 for postgres user so our volumes are
# safe in the future. This should *never* change, the last test is there
# to make sure of that.
# rhel-7-server-ose-3.2-rpms is enabled for nss_wrapper until this pkg is
# in base RHEL
#
# We need to call 2 (!) yum commands before being able to enable repositories properly
# This is a workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1479388
RUN yum repolist > /dev/null && \
    yum install -y yum-utils gettext && \
    yum-config-manager --disable \* &> /dev/null && \
    yum-config-manager --enable rhel-server-rhscl-7-rpms && \
    yum-config-manager --enable rhel-7-server-rpms && \
    yum-config-manager --enable rhel-7-server-optional-rpms && \
    INSTALL_PKGS="rsync tar gettext bind-utils rh-postgresql96 rh-postgresql96-postgresql-contrib nss_wrapper rh-postgresql96-postgresql-server rh-postgresql96-postgresql-devel" && \
    yum -y --setopt=tsflags=nodocs install $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    localedef -f UTF-8 -i en_US en_US.UTF-8 && \
    test "$(id postgres)" = "uid=26(postgres) gid=26(postgres) groups=26(postgres)" && \
    mkdir -p /var/lib/pgsql/data && \
    /usr/libexec/fix-permissions /var/lib/pgsql && \
    /usr/libexec/fix-permissions /var/run/postgresql


# The RHEL Extra Packages for Enterprise Linux (EPEL) package `epel-release`
# is required gdal-libs dependencies.
RUN yum list epel\* && \
    yum list post\* && \
    yum -y install epel-release postgis2_96.x86_64 postgis2_96-client.x86_64 postgis2_96-utils.x86_64 && \
    yum clean all -y


# The install does not put them in the same place as the other PostgreSQL exteions
# so lets move them.
RUN diff --brief -r \
    /opt/rh/rh-postgresql96/root/usr/share/pgsql/extension /usr/pgsql-9.6/share/extension | \
    grep '/usr/pgsql-9.6/share/extension' | \
    tr ':' '/' |  \
    awk '{ print $3 $4 }' | \
    xargs cp -vt /opt/rh/rh-postgresql96/root/usr/share/pgsql/extension && \
    cp -a /usr/pgsql-9.6/share/contrib/* /opt/rh/rh-postgresql96/root/usr/share/pgsql/contrib/ && \
    diff --brief /usr/pgsql-9.6/lib /opt/rh/rh-postgresql96/root/usr/lib64/pgsql | \
    grep -v '/opt/rh/rh-postgresql96/root/usr/lib64/pgsql' | \
    tr ':' '/' |  \
    awk '{ print $3 $4 }' | \
    xargs cp -vt /opt/rh/rh-postgresql96/root/usr/lib64/pgsql && \
    cp -a /usr/pgsql-9.6/bin/pgsql2shp /usr/pgsql-9.6/bin/raster2pgsql \
    /usr/pgsql-9.6/bin/shp2pgsql /opt/rh/rh-postgresql96/root/usr/bin/ && \
    rm -rf /usr/pgsql-9.6


# install dev tools used to compile ORACLE_FDW_2_0_0
RUN yum-config-manager --enable rhel-server-rhscl-7-rpms && \
    yum-config-manager --enable rhel-7-server-rpms && \
    yum-config-manager --enable rhel-7-server-eus-rpms && \
    yum-config-manager --enable rhel-7-server-optional-rpms && \
    yum -y groupinstall 'Development Tools' && \
    yum clean all

# install dev tools used to compile ORACLE_FDW_2_0_0
RUN yum-config-manager --enable rhel-server-rhscl-7-rpms && \
    yum-config-manager --enable rhel-7-server-rpms && \
    yum-config-manager --enable rhel-7-server-eus-rpms && \
    yum-config-manager --enable rhel-7-server-optional-rpms && \
    INSTALL_PKGS="wget libaio-devel" && \
    yum -y --setopt=tsflags=nodocs install $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum clean all


# Get prefix path and path to scripts rather than hard-code them in scripts
ENV CONTAINER_SCRIPTS_PATH=/usr/share/container-scripts/postgresql \
    ENABLED_COLLECTIONS=rh-postgresql96

# When bash is started non-interactively, to run a shell script, for example it
# looks for this variable and source the content of this file. This will enable
# the SCL for all scripts without need to do 'scl enable'.
ENV BASH_ENV=${CONTAINER_SCRIPTS_PATH}/scl_enable \
    ENV=${CONTAINER_SCRIPTS_PATH}/scl_enable \
    PROMPT_COMMAND=". ${CONTAINER_SCRIPTS_PATH}/scl_enable"

VOLUME ["/var/lib/pgsql/data"]

# install the Oracle dependencies.
RUN mkdir -p /tmp/oraclelibs && cd /tmp/oraclelibs && \
    wget -nv https://www.pathfinder.gov.bc.ca/filestore/oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm && \
    wget -nv https://www.pathfinder.gov.bc.ca/filestore/oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64.rpm && \
    rpm -Uvh oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm && \
    rpm -Uvh oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64.rpm

COPY root /

ENV PGCONFIG /opt/rh/rh-postgresql96/root/usr/bin
ENV ORACLE_HOME /usr/lib/oracle/12.2/client64/lib
ENV PATH /opt/rh/rh-postgresql96/root/usr/bin/:${PATH}

# aquire and build ORACLE_FDW_2_0_0
RUN cd /tmp && \
    wget -nv https://github.com/laurenz/oracle_fdw/archive/ORACLE_FDW_2_0_0.tar.gz && \
    tar -xzf ORACLE_FDW_2_0_0.tar.gz && \
    cd oracle_fdw-ORACLE_FDW_2_0_0   && \
    make && \
    make install && \
    rm -rf /tmp/oraclelibs /tmp/ORACLE_FDW_2_0_0.tar.gz /var/cache/yum

# set the oracle library path
ENV LD_LIBRARY_PATH /usr/lib/oracle/12.2/client64/lib:${LD_LIBRARY_PATH}

USER 26

ENTRYPOINT ["container-entrypoint"]
CMD ["run-postgresql"]
