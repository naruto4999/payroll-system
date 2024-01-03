#!/bin/bash

# Define backup filename with timestamp
BACKUP_FILE="/database_backups/db_backup_$(date +%Y-%m-%d_%H-%M-%S).sql"

# Run pg_dump command to backup the database
PGPASSWORD=$POSTGRES_PASSWORD pg_dump -U $POSTGRES_USER -h $DB_HOST $POSTGRES_DB > $BACKUP_FILE