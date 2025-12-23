-- Replace the month literal in params to run a different month.
WITH params AS (
  SELECT '2026-03'::text AS month
),
month_inputs AS (
  SELECT m.*
  FROM months m
  JOIN params p ON m.month = p.month
),
host_base AS (
  SELECT hms.month,
         hms.host_id,
         h.recruiter_id,
         hms.beans,
         hms.tier_base_pay_usd,
         hms.eligible_for_bonus,
         hms.hit_tier_this_month
  FROM host_month_stats hms
  JOIN hosts h ON h.host_id = hms.host_id
  JOIN params p ON hms.month = p.month
),
eligible_totals AS (
  SELECT COALESCE(SUM(CASE WHEN eligible_for_bonus THEN beans ELSE 0 END), 0)
    AS eligible_beans
  FROM host_base
),
host_payouts AS (
  SELECT hb.host_id,
         hb.recruiter_id,
         hb.beans::numeric AS contribution_beans,
         hb.tier_base_pay_usd,
         CASE
           WHEN hb.eligible_for_bonus AND et.eligible_beans > 0
           THEN (hb.beans::numeric / et.eligible_beans)
                * (mi.actual_agency_commission_usd * mi.host_bonus_pool_percent)
           ELSE 0::numeric
         END AS host_bonus_usd
  FROM host_base hb
  CROSS JOIN eligible_totals et
  CROSS JOIN month_inputs mi
),
recruiter_base AS (
  SELECT rms.month,
         rms.recruiter_id,
         rms.active_hosts_count,
         rms.new_qualifying_host_this_month,
         r.is_legacy
  FROM recruiter_month_stats rms
  JOIN recruiters r ON r.recruiter_id = rms.recruiter_id
  JOIN params p ON rms.month = p.month
),
recruiter_eligible AS (
  SELECT rb.*,
         (rb.active_hosts_count >= 3 OR rb.new_qualifying_host_this_month)
           AS eligible_for_recruiter_pool
  FROM recruiter_base rb
),
recruiter_contrib AS (
  SELECT re.recruiter_id,
         re.is_legacy,
         re.active_hosts_count,
         re.new_qualifying_host_this_month,
         re.eligible_for_recruiter_pool,
         CASE
           WHEN re.eligible_for_recruiter_pool
           THEN COALESCE(SUM(CASE WHEN hb.hit_tier_this_month THEN hb.beans ELSE 0 END), 0)
           ELSE 0
         END AS contribution_beans
  FROM recruiter_eligible re
  LEFT JOIN host_base hb ON hb.recruiter_id = re.recruiter_id
  GROUP BY re.recruiter_id,
           re.is_legacy,
           re.active_hosts_count,
           re.new_qualifying_host_this_month,
           re.eligible_for_recruiter_pool
),
total_contrib AS (
  SELECT COALESCE(SUM(contribution_beans), 0) AS total_contribution_beans
  FROM recruiter_contrib
),
recruiter_payouts AS (
  SELECT rc.recruiter_id,
         rc.contribution_beans::numeric AS contribution_beans,
         CASE
           WHEN tc.total_contribution_beans > 0
           THEN (rc.contribution_beans::numeric / tc.total_contribution_beans)
                * (mi.total_agency_gross_usd * mi.recruiter_pool_percent)
           ELSE 0::numeric
         END AS recruiter_pool_share_usd,
         CASE
           WHEN rc.is_legacy
             AND mi.sunset_pool_active
             AND tc.total_contribution_beans > 0
           THEN (rc.contribution_beans::numeric / tc.total_contribution_beans)
                * (mi.actual_agency_commission_usd * mi.sunset_pool_percent)
           ELSE 0::numeric
         END AS sunset_pool_share_usd,
         COALESCE((
           SELECT SUM(hml.amount_usd)
           FROM host_milestone_ledger hml
           WHERE hml.achieved_month = mi.month
             AND hml.recruiter_id = rc.recruiter_id
         ), 0::numeric) AS bounty_payout_usd
  FROM recruiter_contrib rc
  CROSS JOIN total_contrib tc
  CROSS JOIN month_inputs mi
)
SELECT
  mi.month,
  'HOST'::text AS payee_type,
  hp.host_id AS payee_id,
  hp.recruiter_id,
  hp.contribution_beans,
  hp.tier_base_pay_usd,
  hp.host_bonus_usd,
  0::numeric AS recruiter_pool_share_usd,
  0::numeric AS sunset_pool_share_usd,
  0::numeric AS bounty_payout_usd,
  (hp.tier_base_pay_usd + hp.host_bonus_usd) AS total_payout_usd
FROM host_payouts hp
CROSS JOIN month_inputs mi

UNION ALL

SELECT
  mi.month,
  'RECRUITER'::text AS payee_type,
  rp.recruiter_id AS payee_id,
  NULL::text AS recruiter_id,
  rp.contribution_beans,
  0::numeric AS tier_base_pay_usd,
  0::numeric AS host_bonus_usd,
  rp.recruiter_pool_share_usd,
  rp.sunset_pool_share_usd,
  rp.bounty_payout_usd,
  (rp.recruiter_pool_share_usd + rp.sunset_pool_share_usd + rp.bounty_payout_usd)
    AS total_payout_usd
FROM recruiter_payouts rp
CROSS JOIN month_inputs mi
ORDER BY payee_type, payee_id;
