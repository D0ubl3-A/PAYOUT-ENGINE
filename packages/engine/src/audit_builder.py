from decimal import Decimal

from .types import (
    BountyEvent,
    HostMonthRow,
    HostPayout,
    MonthInputs,
    RecruiterMonthRow,
    RecruiterPayout,
    to_decimal,
)


def _decimal_to_str(value: Decimal) -> str:
    return f"{value:.2f}"


def build_audit(
    *,
    inputs: MonthInputs,
    hosts: list[HostMonthRow],
    recruiters: list[RecruiterMonthRow],
    host_payouts: list[HostPayout],
    recruiter_payouts: list[RecruiterPayout],
    host_bonus_pool_usd: Decimal,
    recruiter_pool_usd: Decimal,
    sunset_pool_usd: Decimal,
    eligible_total_beans: int,
    total_recruiter_contribution_beans: int,
    bounty_events: list[BountyEvent],
    contributions: dict[str, int],
) -> dict:
    host_payout_map = {p.host_id: p for p in host_payouts}
    recruiter_payout_map = {p.recruiter_id: p for p in recruiter_payouts}

    host_rows = []
    for host in hosts:
        payout = host_payout_map.get(host.host_id)
        host_rows.append(
            {
                "host_id": host.host_id,
                "recruiter_id": host.recruiter_id,
                "beans": host.beans,
                "eligible_for_bonus": host.eligible_for_bonus,
                "hit_tier_this_month": host.hit_tier_this_month,
                "tier_base_pay_usd": _decimal_to_str(to_decimal(host.tier_base_pay_usd)),
                "host_bonus_usd": _decimal_to_str(payout.host_bonus_usd) if payout else "0.00",
                "host_total_pay_usd": _decimal_to_str(payout.host_total_pay_usd) if payout else "0.00",
            }
        )

    recruiter_rows = []
    for recruiter in recruiters:
        payout = recruiter_payout_map.get(recruiter.recruiter_id)
        recruiter_rows.append(
            {
                "recruiter_id": recruiter.recruiter_id,
                "active_hosts_count": recruiter.active_hosts_count,
                "new_qualifying_host_this_month": recruiter.new_qualifying_host_this_month,
                "legacy_recruiter": recruiter.legacy_recruiter,
                "contribution_beans": contributions.get(recruiter.recruiter_id, 0),
                "recruiter_pool_share_usd": _decimal_to_str(payout.recruiter_pool_share_usd)
                if payout
                else "0.00",
                "sunset_pool_share_usd": _decimal_to_str(payout.sunset_pool_share_usd)
                if payout
                else "0.00",
                "bounty_payout_usd": _decimal_to_str(payout.bounty_payout_usd) if payout else "0.00",
                "total_recruiter_payout_usd": _decimal_to_str(payout.total_recruiter_payout_usd)
                if payout
                else "0.00",
            }
        )

    bounty_rows = [
        {
            "event_id": event.event_id,
            "month": event.month,
            "host_id": event.host_id,
            "recruiter_id": event.recruiter_id,
            "milestone_code": event.milestone_code,
            "amount_usd": _decimal_to_str(to_decimal(event.amount_usd)),
            "note": event.note,
        }
        for event in bounty_events
    ]

    return {
        "version": 1,
        "month": inputs.month,
        "inputs": {
            "actual_agency_commission_usd": _decimal_to_str(
                to_decimal(inputs.actual_agency_commission_usd)
            ),
            "total_agency_gross_usd": _decimal_to_str(to_decimal(inputs.total_agency_gross_usd)),
            "host_bonus_pool_percent": str(inputs.host_bonus_pool_percent),
            "recruiter_pool_percent": str(inputs.recruiter_pool_percent),
            "sunset_pool_percent": str(inputs.sunset_pool_percent),
            "sunset_pool_active": inputs.sunset_pool_active,
        },
        "pools": {
            "host_bonus_pool_usd": _decimal_to_str(host_bonus_pool_usd),
            "recruiter_pool_usd": _decimal_to_str(recruiter_pool_usd),
            "sunset_pool_usd": _decimal_to_str(sunset_pool_usd),
        },
        "totals": {
            "eligible_total_beans": eligible_total_beans,
            "total_recruiter_contribution_beans": total_recruiter_contribution_beans,
        },
        "formulas": {
            "host_bonus_pool_usd": "actual_agency_commission_usd * host_bonus_pool_percent",
            "recruiter_pool_usd": "total_agency_gross_usd * recruiter_pool_percent",
            "sunset_pool_usd": "actual_agency_commission_usd * sunset_pool_percent",
            "host_bonus_usd": "(host.beans / eligible_total_beans) * host_bonus_pool_usd",
            "recruiter_pool_share_usd": (
                "(recruiter_contribution_beans / total_recruiter_contribution_beans)"
                " * recruiter_pool_usd"
            ),
            "sunset_pool_share_usd": (
                "(recruiter_contribution_beans / total_recruiter_contribution_beans)"
                " * sunset_pool_usd"
            ),
            "bounty_payout_usd": "sum(bounty_events.amount_usd for recruiter_id)",
        },
        "hosts": host_rows,
        "recruiters": recruiter_rows,
        "bounty_events": bounty_rows,
    }
