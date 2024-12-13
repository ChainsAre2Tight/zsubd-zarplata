#!/usr/bin/env bash

set +x
set -e

database=zarplata
directory=/usr/src/backups
max_backups=30
backup_server=postgres-server-backup
pwd=root

echo "Starting..."

echo Scanning backup directory at ${directory}...
filecount="$(find ${directory} -type f | wc -l)"

if [[ $filecount -gt $(($max_backups - 1)) ]]
then
    echo There are already ${filecount} backups present '('max ${max_backups}')'

    file_to_delete="$(ls -rt ${directory} | head -n 1)"
    echo Deleting the oldest backup '('${file_to_delete}')'
    rm -- ${directory}/${file_to_delete}
    
    echo Deletion successful
else
    echo There is enough space to create a backup
fi

echo "Starting backup..."
filename=dump-${database}-"`date +"%d-%m-%Y_%H-%M-%S"`"

echo Saving "${database}" to ${filename}
pg_dump ${database} > ${directory}/${filename}
echo "backup successful"

echo Copying dump file to remote at ${backup_server}
sshpass -p ${pwd} scp ${directory}/${filename} ${backup_server}:${directory}/${filename}
echo "Remote copy successful"