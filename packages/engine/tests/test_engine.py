from decimal import Decimal
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.calc_totals import run_payout
from src.types import BountyEvent, HostMonthRow, MonthInputs, RecruiterMonthRow


def test_run_payout_sample_month() -> None:
    inputs = MonthInputs(
        month="2026-03",
        actual_agency_commission_usd=Decimal("1000.00"),
        total_agency_gross_usd=Decimal("5000.00"),
        host_bonus_pool_percent=Decimal("0.60"),
        recruiter_pool_percent=Decimal("0.07"),
        sunset_pool_percent=Decimal("0.15"),
        sunset_pool_active=True,
    )

    hosts = [
        HostMonthRow(
            host_id="H1",
            recruiter_id="R1",
            beans=1000,
            hours_streamed=Decimal("40"),
            tier="T1",
            tier_base_pay_usd=Decimal("100.00"),
            eligible_for_bonus=True,
            hit_tier_this_month=True,
            host_active_months=3,
        ),
        HostMonthRow(
            host_id="H2",
            recruiter_id="R1",
            beans=500,
            hours_streamed=Decimal("35"),
            tier="T1",
            tier_base_pay_usd=Decimal("80.00"),
            eligible_for_bonus=True,
            hit_tier_this_month=False,
            host_active_months=2,
        ),
        HostMonthRow(
            host_id="H3",
            recruiter_id="R2",
            beans=500,
            hours_streamed=Decimal("20"),
            tier="T0",
            tier_base_pay_usd=Decimal("50.00"),
            eligible_for_bonus=False,
            hit_tier_this_month=True,
            host_active_months=3,
        ),
    ]

    recruiters = [
        RecruiterMonthRow(
            recruiter_id="R1",
            active_hosts_count=2,
            new_qualifying_host_this_month=True,
            legacy_recruiter=True,
        ),
        RecruiterMonthRow(
            recruiter_id="R2",
            active_hosts_count=1,
            new_qualifying_host_this_month=False,
            legacy_recruiter=False,
        ),
    ]

    bounty_events = [
        BountyEvent(
            event_id="E1",
            month="2026-03",
            host_id="H1",
            recruiter_id="R1",
            milestone_code="BEANS_5K",
            amount_usd=Decimal("100.00"),
        )
    ]

    result = run_payout(inputs, hosts, recruiters, bounty_events)
    host_map = {p.host_id: p for p in result.host_payouts}
    recruiter_map = {p.recruiter_id: p for p in result.recruiter_payouts}

    assert result.eligible_total_beans == 1500
    assert result.total_recruiter_contribution_beans == 1000

    assert host_map["H1"].host_bonus_usd == Decimal("400.00")
    assert host_map["H1"].host_total_pay_usd == Decimal("500.00")
    assert host_map["H2"].host_bonus_usd == Decimal("200.00")
    assert host_map["H2"].host_total_pay_usd == Decimal("280.00")
    assert host_map["H3"].host_bonus_usd == Decimal("0.00")
    assert host_map["H3"].host_total_pay_usd == Decimal("50.00")

    assert recruiter_map["R1"].recruiter_pool_share_usd == Decimal("350.00")
    assert recruiter_map["R1"].sunset_pool_share_usd == Decimal("150.00")
    assert recruiter_map["R1"].bounty_payout_usd == Decimal("100.00")
    assert recruiter_map["R1"].total_recruiter_payout_usd == Decimal("600.00")
    assert recruiter_map["R2"].total_recruiter_payout_usd == Decimal("0.00")
