#!/bin/bash
psql -U testuser -d test -p 5435 -h localhost -a -f ./sql/seed.sql