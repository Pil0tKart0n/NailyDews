#!/bin/bash
# Daily PostgreSQL backup for NailyDews
# Add to crontab: 0 3 * * * /opt/nailydews/scripts/backup.sh

BACKUP_DIR="/opt/nailydews/backups"
CONTAINER="nailydews-db-1"
DB_USER="nailydews"
DB_NAME="nailydews"
KEEP_DAYS=7

mkdir -p "$BACKUP_DIR"

# Create backup
FILENAME="nailydews-$(date +%Y%m%d-%H%M%S).sql.gz"
docker exec "$CONTAINER" pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_DIR/$FILENAME"

echo "Backup created: $BACKUP_DIR/$FILENAME"

# Delete old backups
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$KEEP_DAYS -delete

echo "Old backups cleaned (keeping $KEEP_DAYS days)"
