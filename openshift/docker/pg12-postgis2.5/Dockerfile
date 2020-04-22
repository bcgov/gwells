FROM registry.access.redhat.com/rhscl/postgresql-12-rhel7:1-10


RUN yum -y install \
		--enablerepo="epel,rhel-7-server-optional-rpms" \
		--setopt=skip_missing_names_on_install=False \
		postgis25_12 \
		postgis25_12-client \
	&& yum -y clean all --enablerepo="epel,rhel-7-server-optional-rpms"

