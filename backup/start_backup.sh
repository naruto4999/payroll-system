#!/bin/bash
chown root:root /backup/backup_script/backup.sh


while true
do
    sleep $((($(date -d '21:30' +%s)-$(date +%s)+86400) % 86400))
    /backup/backup_script/backup.sh
done