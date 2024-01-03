#!/bin/bash
sleep $((($(date -d '21:30' +%s)-$(date +%s)+86400) % 86400))
/backup/backup_script/backup.sh