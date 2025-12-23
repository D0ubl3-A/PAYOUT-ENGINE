BEGIN;

CREATE TABLE recruiters (
  recruiter_id text PRIMARY KEY,
  is_legacy boolean NOT NULL DEFAULT FALSE
);

CREATE TABLE hosts (
  host_id text PRIMARY KEY,
  recruiter_id text REFERENCES recruiters(recruiter_id),
  created_at timestamptz NOT NULL DEFAULT now(),
  is_active boolean NOT NULL DEFAULT TRUE
);

CREATE TABLE months (
  month text PRIMARY KEY,
  actual_agency_commission_usd numeric(12,2) NOT NULL
    CHECK (actual_agency_commission_usd >= 0),
  total_agency_gross_usd numeric(12,2) NOT NULL
    CHECK (total_agency_gross_usd >= 0),
  host_bonus_pool_percent numeric(6,4) NOT NULL
    CHECK (host_bonus_pool_percent >= 0 AND host_bonus_pool_percent <= 1),
  recruiter_pool_percent numeric(6,4) NOT NULL
    CHECK (recruiter_pool_percent >= 0 AND recruiter_pool_percent <= 1),
  sunset_pool_percent numeric(6,4) NOT NULL
    CHECK (sunset_pool_percent >= 0 AND sunset_pool_percent <= 1),
  sunset_pool_active boolean NOT NULL DEFAULT FALSE
);

CREATE TABLE host_month_stats (
  month text NOT NULL REFERENCES months(month) ON DELETE CASCADE,
  host_id text NOT NULL REFERENCES hosts(host_id) ON DELETE CASCADE,
  beans bigint NOT NULL CHECK (beans >= 0),
  hours_streamed numeric(10,2) NOT NULL CHECK (hours_streamed >= 0),
  tier text NOT NULL,
  tier_base_pay_usd numeric(12,2) NOT NULL CHECK (tier_base_pay_usd >= 0),
  eligible_for_bonus boolean NOT NULL,
  hit_tier_this_month boolean NOT NULL,
  host_active_months integer NOT NULL CHECK (host_active_months >= 0),
  PRIMARY KEY (month, host_id)
);

CREATE TABLE recruiter_month_stats (
  month text NOT NULL REFERENCES months(month) ON DELETE CASCADE,
  recruiter_id text NOT NULL REFERENCES recruiters(recruiter_id) ON DELETE CASCADE,
  active_hosts_count integer NOT NULL CHECK (active_hosts_count >= 0),
  new_qualifying_host_this_month boolean NOT NULL,
  PRIMARY KEY (month, recruiter_id)
);

CREATE TABLE bounty_milestones (
  milestone_code text PRIMARY KEY,
  amount_usd numeric(12,2) NOT NULL CHECK (amount_usd >= 0),
  milestone_type text NOT NULL
    CHECK (milestone_type IN ('beans_threshold', 'month_count')),
  threshold_value integer NOT NULL CHECK (threshold_value > 0)
);

CREATE TABLE host_milestone_ledger (
  host_id text NOT NULL REFERENCES hosts(host_id) ON DELETE CASCADE,
  milestone_code text NOT NULL REFERENCES bounty_milestones(milestone_code),
  achieved_month text NOT NULL REFERENCES months(month) ON DELETE CASCADE,
  recruiter_id text REFERENCES recruiters(recruiter_id),
  amount_usd numeric(12,2) NOT NULL CHECK (amount_usd >= 0),
  created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (host_id, milestone_code)
);

CREATE INDEX host_milestone_ledger_month_recruiter_idx
  ON host_milestone_ledger (achieved_month, recruiter_id);

COMMIT;
