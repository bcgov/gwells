FROM crunchydata/crunchy-postgres-gis:centos7-12.2-4.2.2
USER root
RUN yum -y install https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm && \
  yum -y install postgresql96 postgresql96-server && yum -y clean all
USER 26
