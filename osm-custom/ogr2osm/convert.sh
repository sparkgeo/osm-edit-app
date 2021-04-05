#!/bin/sh

IMAGE_NAME=ogr2osm
WORK_DIR=/data
INPUT_DATA=$WORK_DIR/$1
OUTPUT_DATA=$WORK_DIR/$2

echo $INPUT_DATA
echo $OUTPUT_DATA

docker build -t $IMAGE_NAME .

docker run --rm -v $PWD/:/data $IMAGE_NAME $INPUT_DATA -f -o $OUTPUT_DATA
EXIT_CODE=$?

exit $EXIT_CODE
