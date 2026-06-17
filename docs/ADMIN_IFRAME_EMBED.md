# Admin hub iframe embed (IntelliVerse)

ERPNext is embedded inside the IntelliVerse admin portal at `/admin/tools/erpnext`.

## App-level fix (this repo)

`erpnext/utilities/admin_embed.py` runs on every response via Frappe `after_request` in `hooks.py`:

- Removes `X-Frame-Options`
- Sets CSP `frame-ancestors` for:
  - `'self'`
  - `https://admin.intelli-verse-x.ai`
  - `https://admin.toba-tech.ai`
  - `http://localhost:3000`

## Nginx / ingress (required for production)

Live `erp.toba-tech.ai` still returns `X-Frame-Options: SAMEORIGIN` from **nginx** (`server: nginx/1.22.1`). Nginx adds this header **after** the Python app responds, so the Frappe hook alone cannot fix production.

DevOps must update the ingress or bench nginx config. See:

- [`deploy/nginx-admin-iframe.snippet`](../deploy/nginx-admin-iframe.snippet)

### Quick ingress patch

```yaml
metadata:
  annotations:
    nginx.ingress.kubernetes.io/configuration-snippet: |
      proxy_hide_header X-Frame-Options;
      add_header Content-Security-Policy "frame-ancestors 'self' https://admin.intelli-verse-x.ai https://admin.toba-tech.ai http://localhost:3000" always;
```

### Verify

```bash
curl -sI https://erp.toba-tech.ai | grep -iE 'x-frame|content-security'
```

Expected:

- No `X-Frame-Options`
- `Content-Security-Policy` containing `frame-ancestors` and `admin.intelli-verse-x.ai`

## Tests

```bash
python -m unittest erpnext.tests.test_admin_embed
```
