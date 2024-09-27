#!/bin/bash
psql -U admin -d zarplata -p 5435 -h localhost -a -f ./sql/createdb.sql