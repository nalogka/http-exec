#!/bin/sh
if [ -d "/tmp/backup" ]; then
	rm -fr /tmp/backup
fi
mariabackup -u root -p$MYSQL_ROOT_PASSWORD --backup --target-dir=/tmp/backup
tar cz -C /tmp/backup .
rm -fr /tmp/backup
