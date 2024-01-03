#!/bin/bash
sleep $((($(date -d '23:41' +%s)-$(date +%s)+86400) % 86400))
/backup/backup_script/backup.sh