#!/bin/bash

set -e  # Exit immediately if any command fails
set -o pipefail  # Ensure pipes fail correctly
set -u  # Treat unset variables as errors

# Define paths
HOME_DIR=~
PROJECT_DIR="$HOME_DIR/payroll-system"
BACKUP_DIR="$HOME_DIR/backup"
ENV_DIR="$BACKUP_DIR/env_files"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
BACKUP_ZIP="$HOME_DIR/old-payroll-system-$TIMESTAMP.zip"

echo "Starting deployment process..."

# Backup existing project before deletion
if [ -d "$PROJECT_DIR" ]; then
    echo "Creating a backup of the existing project..."
    sudo zip -r "$BACKUP_ZIP" "$PROJECT_DIR"
    echo "Backup saved at $BACKUP_ZIP"
fi

# Remove existing project
echo "Removing existing project..."
sudo rm -rf "$PROJECT_DIR"

# Clone the latest version
echo "Cloning the latest version of the project..."
git clone https://github.com/naruto4999/payroll-system.git "$PROJECT_DIR"

# Restore backup data
echo "Restoring backup data..."
sudo cp -r "$BACKUP_DIR/data" "$PROJECT_DIR"

# Copy environment files
echo "Copying environment files..."
sudo cp "$ENV_DIR/database_env" "$PROJECT_DIR/.env.db"
sudo cp "$ENV_DIR/frontend_env" "$PROJECT_DIR/frontend/.env"
sudo cp "$ENV_DIR/backend_env" "$PROJECT_DIR/backend/payroll_system/.env"

# Ensure deployment scripts are executable after a fresh clone
chmod +x "$PROJECT_DIR/scripts/renew_ssl.sh"

# Navigate to project directory
cd "$PROJECT_DIR"

# Restart the services with Docker Compose
echo "Rebuilding and restarting services..."
docker-compose up -d --build --force-recreate backup database frontend backend

# Run database migrations
echo "Applying database migrations..."
docker-compose exec backend python manage.py migrate --noinput

echo "Deployment completed successfully!"
