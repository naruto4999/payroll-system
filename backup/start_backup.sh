#!/bin/bash
chown root:root /backup/backup_script/backup.sh

sleep $((($(date -d '00:41' +%s)-$(date +%s)+86400) % 86400))
/backup/backup_script/backup.sh