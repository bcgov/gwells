FROM registry.access.redhat.com/rhscl/python-36-rhel7:1-21

USER root

# External libraries required by Python GIS extensions (e.g. GeoDjango, GeoAlchemy)

# Install and configure GEOS 
RUN cd /tmp && wget https://download.osgeo.org/geos/geos-3.7.1.tar.bz2 && \
    tar xjf geos-3.7.1.tar.bz2 && cd geos-3.7.1/ && \
    ./configure --prefix=/usr/local && make && make install && ldconfig && \
    rm -rf /tmp/geos-3.7.1 /tmp/geos-3.7.1.tar.bz2

# Install and configure PROJ.4 
RUN cd /tmp && wget https://download.osgeo.org/proj/proj-5.2.0.tar.gz && \
    wget https://download.osgeo.org/proj/proj-datumgrid-north-america-1.1.tar.gz && \
    tar xzf proj-5.2.0.tar.gz && cd proj-5.2.0/nad && \
    tar xzf ../../proj-datumgrid-north-america-1.1.tar.gz && \
    cd .. && ./configure --prefix=/usr/local && make && make install && ldconfig && \
    rm -rf /tmp/proj-5.2.0 /tmp/proj-5.2.0.tar.gz /tmp/proj-datumgrid-north-america-1.1.tar.gz

# Install and configure GDAL
# (without SFCGAL as we aren't using "CREATE EXTENSION postgis_sfcgal;")
RUN cd /tmp && wget http://download.osgeo.org/gdal/2.4.0/gdal-2.4.0.tar.gz && \
    tar zxvf gdal-2.4.0.tar.gz && cd gdal-2.4.0/ && \
    ./configure --prefix=/usr/local --with-python --with-sfcgal=no && \
    make -j4 && make install && ldconfig && \
    rm -rf /tmp/gdal-2.4.0 /tmp/gdal-2.4.0.tar.gz

USER 1001
