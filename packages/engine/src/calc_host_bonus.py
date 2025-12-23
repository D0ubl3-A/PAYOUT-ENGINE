from decimal import Decimal

from .allocation import allocate_shares
from .types import HostMonthRow, HostPayout, MonthInputs, quantize_money, to_decimal


def calc_host_bonus_pool(inputs: MonthInputs) -> Decimal:
    return to_decimal(inputs.actual_agency_commission_usd) * to_decimal(
        inputs.host_bonus_pool_percent
    )


def calc_host_payouts(
    inputs: MonthInputs,
    hosts: list[HostMonthRow],
    rounding: bool = True,
    pool: Decimal | None = None,
) -> tuple[list[HostPayout], int]:
    eligible_total_beans = sum(host.beans for host in hosts if host.eligible_for_bonus)
    pool_value = pool if pool is not None else calc_host_bonus_pool(inputs)
    if rounding:
        pool_value = quantize_money(pool_value)

    weights = [host.beans if host.eligible_for_bonus else 0 for host in hosts]
    shares = allocate_shares(pool_value, weights, rounding=rounding)

    payouts: list[HostPayout] = []
    for host, share in zip(hosts, shares):
        base_pay = to_decimal(host.tier_base_pay_usd)
        bonus = share
        total = base_pay + bonus
        if rounding:
            total = quantize_money(total)

        payouts.append(
            HostPayout(
                host_id=host.host_id,
                recruiter_id=host.recruiter_id,
                contribution_beans=host.beans,
                tier_base_pay_usd=base_pay,
                host_bonus_usd=bonus,
                host_total_pay_usd=total,
            )
        )

    return payouts, eligible_total_beans
