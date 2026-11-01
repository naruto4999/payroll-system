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

# Update the saved environments before restoring them into the fresh clone.
# Validate all inputs first so an invalid environment cannot trigger deletion
# of the existing project. Never print environment contents (they contain secrets).
echo "Preparing saved production environment files for pay-per.in..."
sudo python3 - "$ENV_DIR" "$TIMESTAMP" <<'PY'
from pathlib import Path
import re
import shlex
import shutil
import sys

env_dir = Path(sys.argv[1])
for name in ("database_env", "frontend_env", "backend_env"):
    if not (env_dir / name).is_file():
        raise SystemExit(f"Missing saved environment file: {name}")

assignment = re.compile(r"^[ \t]*(?:export[ \t]+)?([A-Za-z_][A-Za-z0-9_]*)[ \t]*=(.*)$")


def prepare(text, updates, append=False):
    lines = text.splitlines(keepends=True)
    found = set()
    for index, line in enumerate(lines):
        match = assignment.match(line.rstrip("\r\n"))
        if not match or match[1] not in updates:
            continue
        key = match[1]
        if key in found:
            raise SystemExit(f"Duplicate production environment entry: {key}")
        found.add(key)
        values = updates[key]
        if append:
            existing = " ".join(shlex.split(match[2], comments=True)).split()
            values = list(dict.fromkeys(existing + values))
        lines[index] = f"{key}={' '.join(values)}\n"

    result = "".join(lines)
    for key, values in updates.items():
        if key not in found:
            if result and not result.endswith("\n"):
                result += "\n"
            result += f"{key}={' '.join(values)}\n"
    return result


frontend = env_dir / "frontend_env"
backend = env_dir / "backend_env"
frontend_text = frontend.read_text()
backend_text = backend.read_text()

frontend_updated = prepare(frontend_text, {
    "VITE_BACKEND_URL": ["/"],
    "VITE_PUBLIC_URL": ["/"],
    "VITE_FRONTEND_URL": ["https://pay-per.in/"],
    # Employee photo validation currently expects an absolute HTTP(S) URL.
    "VITE_MEDIA_URL": ["https://pay-per.in"],
})
backend_updated = prepare(backend_text, {
    "ALLOWED_HOSTS": ["pay-per.in", "www.pay-per.in"],
    "CORS_ALLOWED_ORIGINS": ["https://pay-per.in", "https://www.pay-per.in"],
    "CSRF_TRUSTED_ORIGINS": ["https://pay-per.in", "https://www.pay-per.in"],
}, append=True)
# Static assets are served by Nginx on either domain; do not retain the old
# absolute .me URL or append to it as if it were a host/origin list.
backend_updated = prepare(backend_updated, {"STATIC_URL": ["/static/"]})

changes = [
    (frontend, frontend_text, frontend_updated),
    (backend, backend_text, backend_updated),
]
changes = [item for item in changes if item[1] != item[2]]
if changes:
    backup_dir = env_dir / f"before-domain-update-{sys.argv[2]}"
    backup_dir.mkdir(mode=0o700)
    for path, _, _ in changes:
        shutil.copy2(path, backup_dir / path.name)
    for path, _, updated in changes:
        path.write_text(updated)
    print("Updated saved production URLs and domain lists; previous files backed up.")
else:
    print("Saved production domain settings are already current.")
PY

# Backup existing project before deletion
if [ -d "$PROJECT_DIR" ]; then
    echo "Creating a backup of the existing project..."
    sudo bash -c 'umask 077; exec zip -r -y "$1" "$2"' bash "$BACKUP_ZIP" "$PROJECT_DIR"
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

# Cron invokes this path outside the clone. Refresh it on every deployment.
echo "Installing the current SSL renewal script..."
install -m 700 "$PROJECT_DIR/scripts/renew_ssl.sh" "$HOME_DIR/renew_ssl.sh"

# Navigate to project directory
cd "$PROJECT_DIR"

# Restart the services with Docker Compose
echo "Rebuilding and restarting services..."
docker-compose up -d --build --force-recreate backup database frontend backend

# Run database migrations
echo "Applying database migrations..."
docker-compose exec backend python manage.py migrate --noinput

echo "Deployment completed successfully!"
