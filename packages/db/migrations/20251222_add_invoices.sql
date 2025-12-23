BEGIN;

CREATE TABLE invoices (
  invoice_id text PRIMARY KEY,
  run_id text NOT NULL REFERENCES payout_runs(run_id) ON DELETE CASCADE,
  month text NOT NULL REFERENCES months(month) ON DELETE RESTRICT,
  recipient_type text NOT NULL
    CHECK (recipient_type IN ('host', 'recruiter')),
  recipient_id text NOT NULL,
  invoice_number text NOT NULL,
  status text NOT NULL
    CHECK (status IN ('READY', 'FAILED')),
  file_format text NOT NULL
    CHECK (file_format IN ('html')),
  filename text NOT NULL,
  content_type text NOT NULL,
  storage_path text NOT NULL,
  size_bytes bigint NOT NULL CHECK (size_bytes >= 0),
  sha256 text NOT NULL,
  total_usd numeric(12,2) NOT NULL CHECK (total_usd >= 0),
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX invoices_run_idx ON invoices (run_id);
CREATE INDEX invoices_recipient_idx ON invoices (recipient_type, recipient_id, month);

COMMIT;
