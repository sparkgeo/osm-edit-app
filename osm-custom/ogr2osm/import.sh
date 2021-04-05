#!/bin/sh

osmosis --read-xml $1 \
  --write-apidb host="db" database="openstreetmap" \
  user="postgrtes" password="postgres" validateSchemaVersion="no"