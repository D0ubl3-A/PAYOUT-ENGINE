from decimal import Decimal

from .allocation import allocate_shares
from .types import MonthInputs, RecruiterMonthRow, quantize_money, to_decimal


def calc_sunset_pool(inputs: MonthInputs) -> Decimal:
    return to_decimal(inputs.actual_agency_commission_usd) * to_decimal(inputs.sunset_pool_percent)


def calc_sunset_pool_shares(
    inputs: MonthInputs,
    recruiters: list[RecruiterMonthRow],
    contributions: dict[str, int],
    rounding: bool = True,
    pool: Decimal | None = None,
) -> tuple[dict[str, Decimal], Decimal]:
    pool_value = pool if pool is not None else calc_sunset_pool(inputs)
    if rounding:
        pool_value = quantize_money(pool_value)

    recruiter_ids = [recruiter.recruiter_id for recruiter in recruiters]
    weights = []
    for recruiter in recruiters:
        if inputs.sunset_pool_active and recruiter.legacy_recruiter:
            weights.append(contributions.get(recruiter.recruiter_id, 0))
        else:
            weights.append(0)

    shares = allocate_shares(pool_value, weights, rounding=rounding)
    return dict(zip(recruiter_ids, shares)), pool_value
