#!/bin/bash
set -uo pipefail

echo "========== $(date -u '+%Y-%m-%d %H:%M:%S UTC') SSL renewal started =========="

cd /home/kaushal/payroll-system

renew_status=0
docker-compose run --rm certbot renew || renew_status=$?

backup_status=0
docker-compose run --rm ssl-data-backup || backup_status=$?

docker-compose down
docker-compose up -d frontend backend backup database

echo "Renew status: $renew_status"
echo "Backup copy status: $backup_status"
echo "========== $(date -u '+%Y-%m-%d %H:%M:%S UTC') SSL renewal finished =========="

exit "$((renew_status != 0 || backup_status != 0))"
