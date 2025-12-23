from decimal import Decimal

from .audit_builder import build_audit
from .calc_host_bonus import calc_host_bonus_pool, calc_host_payouts
from .calc_recruiter_pool import (
    calc_recruiter_contributions,
    calc_recruiter_pool,
    calc_recruiter_pool_shares,
)
from .calc_sunset_pool import calc_sunset_pool, calc_sunset_pool_shares
from .types import (
    BountyEvent,
    EngineResult,
    HostMonthRow,
    MonthInputs,
    RecruiterMonthRow,
    RecruiterPayout,
    quantize_money,
    to_decimal,
)
from .validators import validate_inputs, validate_pool_sum


def sum_payouts(values: list[Decimal]) -> Decimal:
    total = Decimal("0")
    for value in values:
        total += value
    return total


def sum_bounties_by_recruiter(
    bounty_events: list[BountyEvent],
    month: str,
) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = {}
    for event in bounty_events:
        if event.month != month:
            continue
        amount = to_decimal(event.amount_usd)
        totals[event.recruiter_id] = totals.get(event.recruiter_id, Decimal("0")) + amount
    return totals


def run_payout(
    inputs: MonthInputs,
    hosts: list[HostMonthRow],
    recruiters: list[RecruiterMonthRow],
    bounty_events: list[BountyEvent],
    rounding: bool = True,
    tolerance: Decimal = Decimal("0.01"),
) -> EngineResult:
    validate_inputs(inputs, hosts, recruiters, bounty_events)

    host_bonus_pool_usd = calc_host_bonus_pool(inputs)
    if rounding:
        host_bonus_pool_usd = quantize_money(host_bonus_pool_usd)
    host_payouts, eligible_total_beans = calc_host_payouts(
        inputs, hosts, rounding=rounding, pool=host_bonus_pool_usd
    )

    contributions, total_recruiter_contribution_beans = calc_recruiter_contributions(
        hosts, recruiters
    )
    recruiter_pool_usd = calc_recruiter_pool(inputs)
    if rounding:
        recruiter_pool_usd = quantize_money(recruiter_pool_usd)
    recruiter_pool_shares, recruiter_pool_usd = calc_recruiter_pool_shares(
        inputs, contributions, rounding=rounding, pool=recruiter_pool_usd
    )

    sunset_pool_usd = calc_sunset_pool(inputs)
    if rounding:
        sunset_pool_usd = quantize_money(sunset_pool_usd)
    sunset_pool_shares, sunset_pool_usd = calc_sunset_pool_shares(
        inputs, recruiters, contributions, rounding=rounding, pool=sunset_pool_usd
    )

    bounty_totals = sum_bounties_by_recruiter(bounty_events, inputs.month)

    recruiter_payouts: list[RecruiterPayout] = []
    for recruiter in recruiters:
        recruiter_id = recruiter.recruiter_id
        contribution = contributions.get(recruiter_id, 0)
        recruiter_pool_share = recruiter_pool_shares.get(recruiter_id, Decimal("0"))
        sunset_pool_share = sunset_pool_shares.get(recruiter_id, Decimal("0"))
        bounty_payout = bounty_totals.get(recruiter_id, Decimal("0"))
        if rounding:
            bounty_payout = quantize_money(bounty_payout)

        total = recruiter_pool_share + sunset_pool_share + bounty_payout
        if rounding:
            total = quantize_money(total)

        recruiter_payouts.append(
            RecruiterPayout(
                recruiter_id=recruiter_id,
                contribution_beans=contribution,
                recruiter_pool_share_usd=recruiter_pool_share,
                sunset_pool_share_usd=sunset_pool_share,
                bounty_payout_usd=bounty_payout,
                total_recruiter_payout_usd=total,
            )
        )

    if eligible_total_beans > 0:
        validate_pool_sum(
            host_bonus_pool_usd,
            [p.host_bonus_usd for p in host_payouts],
            "host_bonus_pool_usd",
            tolerance,
        )

    if total_recruiter_contribution_beans > 0:
        validate_pool_sum(
            recruiter_pool_usd,
            [p.recruiter_pool_share_usd for p in recruiter_payouts],
            "recruiter_pool_usd",
            tolerance,
        )

        legacy_recruiters = [r for r in recruiters if r.legacy_recruiter]
        if inputs.sunset_pool_active and legacy_recruiters:
            validate_pool_sum(
                sunset_pool_usd,
                [p.sunset_pool_share_usd for p in recruiter_payouts],
                "sunset_pool_usd",
                tolerance,
            )

    audit = build_audit(
        inputs=inputs,
        hosts=hosts,
        recruiters=recruiters,
        host_payouts=host_payouts,
        recruiter_payouts=recruiter_payouts,
        host_bonus_pool_usd=host_bonus_pool_usd,
        recruiter_pool_usd=recruiter_pool_usd,
        sunset_pool_usd=sunset_pool_usd,
        eligible_total_beans=eligible_total_beans,
        total_recruiter_contribution_beans=total_recruiter_contribution_beans,
        bounty_events=bounty_events,
        contributions=contributions,
    )

    return EngineResult(
        month=inputs.month,
        host_bonus_pool_usd=host_bonus_pool_usd,
        recruiter_pool_usd=recruiter_pool_usd,
        sunset_pool_usd=sunset_pool_usd,
        eligible_total_beans=eligible_total_beans,
        total_recruiter_contribution_beans=total_recruiter_contribution_beans,
        host_payouts=host_payouts,
        recruiter_payouts=recruiter_payouts,
        audit=audit,
    )
