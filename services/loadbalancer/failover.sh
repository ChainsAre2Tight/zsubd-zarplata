#!/bin/bash

echo "promoting slave to master"
echo connecting

sshpass -p postgres ssh postgres@postgres-server-slave "pg_ctl promote"