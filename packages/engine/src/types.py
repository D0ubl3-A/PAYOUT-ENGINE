from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable

MONEY_QUANT = Decimal("0.01")


def to_decimal(value: Decimal | int | float | str) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def quantize_money(value: Decimal) -> Decimal:
    return value.quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)


def sum_decimals(values: Iterable[Decimal]) -> Decimal:
    total = Decimal("0")
    for value in values:
        total += to_decimal(value)
    return total


@dataclass(frozen=True)
class MonthInputs:
    month: str
    actual_agency_commission_usd: Decimal
    total_agency_gross_usd: Decimal
    host_bonus_pool_percent: Decimal
    recruiter_pool_percent: Decimal
    sunset_pool_percent: Decimal
    sunset_pool_active: bool


@dataclass(frozen=True)
class HostMonthRow:
    host_id: str
    recruiter_id: str | None
    beans: int
    hours_streamed: Decimal
    tier: str
    tier_base_pay_usd: Decimal
    eligible_for_bonus: bool
    hit_tier_this_month: bool
    host_active_months: int


@dataclass(frozen=True)
class RecruiterMonthRow:
    recruiter_id: str
    active_hosts_count: int
    new_qualifying_host_this_month: bool
    legacy_recruiter: bool


@dataclass(frozen=True)
class BountyEvent:
    event_id: str
    month: str
    host_id: str
    recruiter_id: str
    milestone_code: str
    amount_usd: Decimal
    note: str | None = None


@dataclass(frozen=True)
class MilestoneDefinition:
    milestone_code: str
    milestone_type: str
    threshold_value: int
    amount_usd: Decimal


@dataclass(frozen=True)
class MilestoneLedgerEntry:
    host_id: str
    milestone_code: str
    achieved_month: str
    recruiter_id: str | None
    amount_usd: Decimal


@dataclass(frozen=True)
class HostPayout:
    host_id: str
    recruiter_id: str | None
    contribution_beans: int
    tier_base_pay_usd: Decimal
    host_bonus_usd: Decimal
    host_total_pay_usd: Decimal


@dataclass(frozen=True)
class RecruiterPayout:
    recruiter_id: str
    contribution_beans: int
    recruiter_pool_share_usd: Decimal
    sunset_pool_share_usd: Decimal
    bounty_payout_usd: Decimal
    total_recruiter_payout_usd: Decimal


@dataclass(frozen=True)
class EngineResult:
    month: str
    host_bonus_pool_usd: Decimal
    recruiter_pool_usd: Decimal
    sunset_pool_usd: Decimal
    eligible_total_beans: int
    total_recruiter_contribution_beans: int
    host_payouts: list[HostPayout]
    recruiter_payouts: list[RecruiterPayout]
    audit: dict
