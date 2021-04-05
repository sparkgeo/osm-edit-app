FROM osgeo/gdal:ubuntu-small-3.1.0

RUN apt-get -y update \
    && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /source
WORKDIR /source

RUN git clone --recursive https://github.com/pnorman/ogr2osm

ENTRYPOINT [ "/source/ogr2osm/ogr2osm.py" ]