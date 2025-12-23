from decimal import Decimal

from .allocation import allocate_shares
from .types import HostMonthRow, MonthInputs, RecruiterMonthRow, quantize_money, to_decimal


def recruiter_is_eligible(recruiter: RecruiterMonthRow) -> bool:
    return recruiter.active_hosts_count >= 3 or recruiter.new_qualifying_host_this_month


def calc_recruiter_pool(inputs: MonthInputs) -> Decimal:
    return to_decimal(inputs.total_agency_gross_usd) * to_decimal(inputs.recruiter_pool_percent)


def calc_recruiter_contributions(
    hosts: list[HostMonthRow],
    recruiters: list[RecruiterMonthRow],
) -> tuple[dict[str, int], int]:
    contributions: dict[str, int] = {}
    for recruiter in recruiters:
        if recruiter_is_eligible(recruiter):
            beans = sum(
                host.beans
                for host in hosts
                if host.recruiter_id == recruiter.recruiter_id and host.hit_tier_this_month
            )
        else:
            beans = 0
        contributions[recruiter.recruiter_id] = beans

    total_contribution = sum(contributions.values())
    return contributions, total_contribution


def calc_recruiter_pool_shares(
    inputs: MonthInputs,
    contributions: dict[str, int],
    rounding: bool = True,
    pool: Decimal | None = None,
) -> tuple[dict[str, Decimal], Decimal]:
    pool_value = pool if pool is not None else calc_recruiter_pool(inputs)
    if rounding:
        pool_value = quantize_money(pool_value)

    recruiter_ids = list(contributions.keys())
    weights = [contributions[recruiter_id] for recruiter_id in recruiter_ids]
    shares = allocate_shares(pool_value, weights, rounding=rounding)

    return dict(zip(recruiter_ids, shares)), pool_value
