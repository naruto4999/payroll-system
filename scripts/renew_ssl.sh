#!/bin/bash
set -uo pipefail

echo "========== $(date -u '+%Y-%m-%d %H:%M:%S UTC') SSL renewal started =========="

cd "${PAYROLL_PROJECT_DIR:-/home/kaushal/payroll-system}" || exit 1

renew_status=0
docker-compose run --rm --no-deps certbot renew || renew_status=$?

# A partial renewal can update one certificate even if another fails. Always
# attempt to load valid certificate files, while still reporting renewal errors.
reload_status=0
if docker-compose exec -T frontend nginx -t; then
    docker-compose exec -T frontend nginx -s reload || reload_status=$?
else
    reload_status=1
fi

backup_status=0
docker-compose run --rm --no-deps ssl-data-backup || backup_status=$?

echo "Renew status: $renew_status"
echo "Nginx validation/reload status: $reload_status"
echo "Backup copy status: $backup_status"
echo "========== $(date -u '+%Y-%m-%d %H:%M:%S UTC') SSL renewal finished =========="

exit "$((renew_status != 0 || reload_status != 0 || backup_status != 0))"
