# Vercel Deployment

This repo contains two Next.js apps:
- `apps/admin-web`
- `apps/host-web`

The FastAPI backend should be deployed separately (it handles Groq vision + file uploads).

## Vercel projects (UI)

Create two Vercel projects and point each to the correct root:

1) Admin UI
   - Root Directory: `apps/admin-web`
   - `vercel.json` already included in the app root.
   - Build Command: `npm run build`
   - Output: `.next`
   - Environment:
     - `NEXT_PUBLIC_API_URL=https://<your-api-domain>`
     - `API_BASE_URL=https://<your-api-domain>`

2) Host UI
   - Root Directory: `apps/host-web`
   - `vercel.json` already included in the app root.
   - Build Command: `npm run build`
   - Output: `.next`
   - Environment:
     - `NEXT_PUBLIC_API_URL=https://<your-api-domain>`
     - `API_BASE_URL=https://<your-api-domain>`

## Backend deployment (recommended)

- Deploy `services/api` to a container host (Render, Fly, etc.).
- Set env vars: `DATABASE_URL`, `GROQ_API_KEY`, storage config, `CORS_ORIGINS`.
- Invoice settings (HTML output):
  - `INVOICE_ISSUER_NAME`, `INVOICE_ISSUER_EMAIL`, `INVOICE_ISSUER_ADDRESS`
  - `INVOICE_PAYMENT_TERMS`, `INVOICE_CURRENCY`, `INVOICE_NUMBER_PREFIX`
- Point `NEXT_PUBLIC_API_URL` to the backend domain.

## CORS

Set `CORS_ORIGINS` on the API to your Vercel app domains, comma-separated:

```
https://<admin-app>.vercel.app,https://<host-app>.vercel.app
```

## Database migration (existing DBs)

If the database already exists, apply the invoice migration:

```
packages/db/migrations/20251222_add_invoices.sql
```
