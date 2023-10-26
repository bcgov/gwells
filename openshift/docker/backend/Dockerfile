FROM registry.access.redhat.com/ubi8/python-38:1-131

# Switch to root user
#
USER root

# NPROC Gets number of processing units available to system, speeding up build. 
ENV NPROC 3

# External libraries required by Python GIS extensions (e.g. GeoDjango, GeoAlchemy)
# Install and configure GEOS
#
# Note: HTTPS will result in certificate errors, hence the downgrade to HTTP here
#

WORKDIR /tmp

RUN NPROC=${NPROC} && \
    wget http://download.osgeo.org/geos/geos-3.7.1.tar.bz2 && \
    tar xjf geos-3.7.1.tar.bz2 && \
    cd geos-3.7.1/ && \
    ./configure --prefix=/usr/local && \
    make -j"$NPROC" && \
    make install && \
    ldconfig && \
    cd /tmp && \
    rm -rf /tmp/geos-3.7.1 /tmp/geos-3.7.1.tar.bz2


# Install and configure PROJ.4
#
# Note: HTTPS will result in certificate errors, hence the downgrade to HTTP here
#

RUN wget http://download.osgeo.org/proj/proj-6.0.0.tar.gz && \
    wget http://download.osgeo.org/proj/proj-datumgrid-north-america-1.4.tar.gz && \
    tar xzf proj-6.0.0.tar.gz && \
    cd proj-6.0.0 && \
    tar xzf ../proj-datumgrid-north-america-1.4.tar.gz && \
    ./configure --prefix=/usr/local && \
    make -j"$NPROC" \
    && make install && \
    ldconfig && \
    rm -rf /tmp/proj-6.0.0 /tmp/proj-6.0.0.tar.gz /tmp/proj-datumgrid-north-america-1.4.tar.gz


# Install and configure GDAL
# (without SFCGAL as we aren't using "CREATE EXTENSION postgis_sfcgal;")
#

RUN wget http://download.osgeo.org/gdal/3.0.4/gdal-3.0.4.tar.gz && \
    tar zxvf gdal-3.0.4.tar.gz && cd gdal-3.0.4/ && \
    ./configure --prefix=/usr/local --with-python --with-sfcgal=no && \
    make -j4 && \
    make install && \
    ldconfig && \
    rm -rf /tmp/gdal-3.0.4 /tmp/gdal-3.0.4.tar.gz


WORKDIR /

# Configure GDAL file locations
#
RUN echo "/usr/local/lib/" >> /etc/ld.so.conf && \
    ldconfig


USER 1001
