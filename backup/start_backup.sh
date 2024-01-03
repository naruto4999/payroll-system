#!/bin/bash
sleep $((($(date -d '4:32' +%s)-$(date +%s)+86400) % 86400))
/backup/backup_script/backup.sh