#!/bin/bash
docker exec -it postgres-client psql -h postgres-server -a -f createdb.sql