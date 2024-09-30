#!/bin/bash
docker exec -it psql -h postgres-server -a -f createdb.sql