from decimal import Decimal

from .types import (
    BountyEvent,
    HostMonthRow,
    MonthInputs,
    RecruiterMonthRow,
    sum_decimals,
    to_decimal,
)


def ensure_non_negative(value: Decimal | int | float, field: str) -> None:
    if to_decimal(value) < 0:
        raise ValueError(f"{field} must be >= 0")


def ensure_percent(value: Decimal | int | float, field: str) -> None:
    numeric = to_decimal(value)
    if numeric < 0 or numeric > 1:
        raise ValueError(f"{field} must be between 0 and 1")


def validate_inputs(
    inputs: MonthInputs,
    hosts: list[HostMonthRow],
    recruiters: list[RecruiterMonthRow],
    bounty_events: list[BountyEvent],
) -> None:
    ensure_non_negative(inputs.actual_agency_commission_usd, "actual_agency_commission_usd")
    ensure_non_negative(inputs.total_agency_gross_usd, "total_agency_gross_usd")
    ensure_percent(inputs.host_bonus_pool_percent, "host_bonus_pool_percent")
    ensure_percent(inputs.recruiter_pool_percent, "recruiter_pool_percent")
    ensure_percent(inputs.sunset_pool_percent, "sunset_pool_percent")

    for host in hosts:
        ensure_non_negative(host.beans, f"{host.host_id}.beans")
        ensure_non_negative(host.hours_streamed, f"{host.host_id}.hours_streamed")
        ensure_non_negative(host.tier_base_pay_usd, f"{host.host_id}.tier_base_pay_usd")
        ensure_non_negative(host.host_active_months, f"{host.host_id}.host_active_months")

    for recruiter in recruiters:
        ensure_non_negative(
            recruiter.active_hosts_count, f"{recruiter.recruiter_id}.active_hosts_count"
        )

    for event in bounty_events:
        ensure_non_negative(event.amount_usd, f"{event.event_id}.amount_usd")


def validate_pool_sum(
    pool_usd: Decimal,
    shares: list[Decimal],
    field: str,
    tolerance: Decimal,
) -> None:
    if abs(sum_decimals(shares) - pool_usd) > tolerance:
        raise ValueError(f"{field} shares do not sum to pool within tolerance")
