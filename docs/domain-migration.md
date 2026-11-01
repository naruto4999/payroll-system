# pay-per.in migration

The droplet has separate Certbot certificates for `pay-per.in` / `www.pay-per.in`
and `pay-per.me` / `www.pay-per.me`. Both must exist before activating this Nginx
configuration. Do not run `init-letsencrypt.sh` on this existing deployment.

## Deploy with a frontend rebuild

The production frontend has already been rebuilt with `VITE_BACKEND_URL=/`.
Its current and saved backend environments allow both domains. Preserve those
environment files when transferring the migration files.

### Normal deployment with scripts/deploy.sh

Use the updated `scripts/deploy.sh` for future deployments. If you launch a
separate copy such as `~/deploy.sh`, refresh that copy first. The script now:

1. Checks that all three saved environment files exist before deleting anything.
2. Updates `~/backup/env_files/frontend_env` with these production URLs:

   ```dotenv
   VITE_BACKEND_URL=/
   VITE_PUBLIC_URL=/
   VITE_FRONTEND_URL=https://pay-per.in/
   VITE_MEDIA_URL=https://pay-per.in
   ```

   The frontend origin is used in password-reset emails. The media origin has
   no trailing slash because employee photo paths already begin with `/media/`.
3. Adds the `.in` root and `www` hostnames/origins to the saved backend domain
   lists without removing existing entries. In particular, `.me` keeps working
   during the transition. Sets `STATIC_URL=/static/` in the saved backend
   environment so Django admin/static assets do not depend on `.me`.
   No database or SMTP credentials are changed.
4. Backs up changed saved environments in a private
   `~/backup/env_files/before-domain-update-*` directory.
5. Restores those updated environments into the fresh clone before building.
6. Copies the repository renewal script to `~/renew_ssl.sh`, the existing cron
   target, on every deployment.

The tracked examples `frontend/.env.production.example`,
`backend/payroll_system/.env.production.example`, and `.env.db.example` document
the required configuration. They are references, not replacements for existing
production secrets. The developer's ignored local `.env` files remain configured
for localhost; Django reads domain lists from the environment rather than
hardcoding production domains in `settings.py`.

### Manual frontend-only deployment

Transfer these files into the same relative paths in
`/home/kaushal/payroll-system`:

- `docker-compose.yml`
- `frontend/nginx.conf`
- `frontend/public/domain-moved.html`
- `scripts/renew_ssl.sh`

Nginx configuration is copied into the frontend image by its Dockerfile. Vite
copies the notice from `frontend/public/` into the built site. Rebuild the image
to apply changes to either file; there are no extra configuration bind mounts.

From the project directory, build and validate before replacing the frontend.
The database and backend must be running for Nginx to resolve `backend`:

```bash
cd /home/kaushal/payroll-system
docker-compose build frontend
docker-compose run --rm --no-deps frontend nginx -t
docker-compose up -d --no-deps --force-recreate frontend
```

Run each command only after the previous one succeeds. This briefly restarts
the frontend without restarting the database or backend.

On a resource-constrained droplet, stop the stack before building. The site
will be unavailable until it is restarted:

```bash
docker-compose stop frontend backend backup database
docker-compose build frontend
docker-compose up -d database backend
docker-compose run --rm --no-deps frontend nginx -t
docker-compose up -d frontend backup
```

Stop if the build or validation fails. Do not remove the named data volumes.

## Update the existing cron script for a manual deployment

`scripts/deploy.sh` does this automatically. If deploying only the frontend
manually, rebuilding does not update the script outside the repository. Copy
the updated renewal script to the existing cron target:

```bash
cp -p /home/kaushal/renew_ssl.sh "/home/kaushal/renew_ssl.sh.backup-$(date -u +%Y%m%d-%H%M%S)"
bash -n scripts/renew_ssl.sh
install -m 700 scripts/renew_ssl.sh /home/kaushal/renew_ssl.sh
```

The original cron entry remains Thursday 20:30 UTC (Friday 02:00 IST). The new
script validates and reloads Nginx and backs up certificate data, reporting
failures without taking down the stack. A partial renewal still triggers
validation/reload because another domain may have renewed successfully.
Repeat the copy whenever the repository renewal script changes and you are not
using `scripts/deploy.sh`.

## Verify

```bash
curl -I https://pay-per.in/login
curl -I https://pay-per.me/login
curl -I https://www.pay-per.me/login
docker-compose run --rm --no-deps certbot renew --dry-run
```

Check in a browser that `.me/login` shows the notice, has `Cache-Control:
no-store`, and redirects to `.in/login` after 10 seconds. Check the immediate
button, keyboard navigation, and new-domain login. Query strings and fragments
are deliberately not transferred. Without JavaScript the button still works.
Existing `.me` API, admin, assets, media and static routes stay available for
the transition; HTTP ACME challenges remain accessible on both domains.

For later Nginx or notice-page edits, repeat the frontend build, validation,
and recreation commands above. Reloading alone cannot pick up source files
that have not been copied into a rebuilt image.

These changes must reach the Git remote through the normal reviewed commit /
deployment workflow before using `scripts/deploy.sh`, which deletes the project
directory and clones that remote. Merely copying them to the droplet does not
update the remote. No environment files or certificate backups belong in Git.

## Cloudflare

Once the origin works, set the `.in` zone SSL/TLS mode to **Full (strict)**,
confirm its edge certificate is active, then enable proxying for the root A
record and `www` CNAME. Retest login, downloads, and renewal challenge handling.
Ensure any configured cache rules do not cache the old-domain notice or API.

## Retire the old domain before expiry

The notice cannot be relied on after `.me` expires on 10 November 2026. Tell
users directly to update their bookmarks before then.

1. Remove the two `.me` server blocks from `frontend/nginx.conf`.
2. Rebuild, validate, and recreate the frontend as above, and confirm `.in` works.
3. Remove the old lineage with
   `docker-compose run --rm --no-deps certbot delete --cert-name pay-per.me`.
   Do not delete it while Nginx still references its files.
4. Remove `.me` hosts/origins from both the active backend environment and
   `~/backup/env_files/backend_env`, then recreate the backend and reload Nginx
   so it resolves the replacement backend container.
5. Refresh `ssl-data-backup` and verify `.in` renewal separately with
   `docker-compose run --rm --no-deps certbot renew --cert-name pay-per.in --dry-run`.

Migrate Jellyfin separately. Its new hostname requires either updating the
Cloudflare Tunnel public hostname/ingress or the home DNS/reverse-proxy/TLS
configuration, depending on how the local server is exposed.
