#!/bin/sh
if [ -d "/tmp/backup" ]; then
	rm -fr /tmp/backup
fi
EXCLUDE_DB="nalogka-sandbox_core-deals nalogka-sandbox_delivery-cdek nalogka-sandbox_depositary-b2p nalogka-sandbox_users nalogka_admin_sandbox nalogka_delivery_cdek_sandbox"
mariabackup -u root -p$MYSQL_ROOT_PASSWORD --backup --databases-exclude="$EXCLUDE_DB" --target-dir=/tmp/backup
tar cz -C /tmp/backup .
rm -fr /tmp/backup