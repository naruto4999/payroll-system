# Google Drive Database Backup Plan

Date: 2026-07-12

## Goal

Copy daily PostgreSQL database backups from the VPS to Google Drive automatically.

## Recommended Tool

Use `rclone` on the VPS.

`rclone` supports Google Drive, works well with cron, and can copy only new or changed files.

## Recommended Flow

Keep database backup and Google Drive upload separate.

Suggested timing:

- Local DB backup runs around 3:00 AM IST.
- Google Drive upload runs around 3:30 AM IST.

Since cron is using UTC:

- 3:30 AM IST = 22:00 UTC previous day.

## Backup Location

Local backups are expected to be stored in:

```text
/home/kaushal/database_backups
```

Google Drive destination:

```text
gdrive:payroll-system/database_backups
```

## Why Use `rclone copy`

Use:

```bash
rclone copy
```

Do not use:

```bash
rclone sync
```

Reason: `sync` can delete files from Google Drive if they are missing locally. For backups, `copy` is safer.

## Setup Steps

Install rclone:

```bash
sudo apt install rclone
```

Configure Google Drive:

```bash
rclone config
```

Create a remote named:

```text
gdrive
```

Verify access:

```bash
rclone lsd gdrive:
```

Dry-run upload test:

```bash
rclone copy /home/kaushal/database_backups gdrive:payroll-system/database_backups --include "*.sql" --dry-run
```

If dry run looks correct, run without `--dry-run`.

## Cron Job

Edit crontab:

```bash
crontab -e
```

Add:

```cron
0 22 * * * rclone copy /home/kaushal/database_backups gdrive:payroll-system/database_backups --include "*.sql" --log-file /home/kaushal/rclone-db-backup.log --log-level INFO
```

Verify cron:

```bash
crontab -l
```

Check logs:

```bash
tail -100 /home/kaushal/rclone-db-backup.log
```

## Optional Cleanup

After confirming Google Drive uploads are reliable, local old backups can be deleted automatically.

Example: keep only 14 days locally.

```bash
find /home/kaushal/database_backups -name "*.sql" -mtime +14 -delete
```

Do not add cleanup until remote backups are verified.

## Recommendation

Use this setup:

- `rclone copy`
- Daily upload at 22:00 UTC / 3:30 AM IST
- Separate cron from database backup
- Keep local backups for 7-14 days
- Keep Google Drive backups long-term
