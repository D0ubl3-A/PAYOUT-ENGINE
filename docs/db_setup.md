# DB Setup

## Option A: Docker Compose (no local psql required)

```bash
docker compose up -d postgres
docker compose exec -T postgres psql -U postgres -d payout < packages/db/schema.sql
```

## Option B: Local Postgres + psql

```bash
psql "$DATABASE_URL" -f packages/db/schema.sql
```

## Convenience script (PowerShell)

```powershell
.\scripts\setup_db.ps1
```
