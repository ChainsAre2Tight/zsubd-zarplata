#!/bin/bash
psql -U admin -d zarplata 5435 -h localhost -a -f ./sql/seed.sql