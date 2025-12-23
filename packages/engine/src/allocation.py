from decimal import Decimal, ROUND_HALF_UP

from .types import MONEY_QUANT, quantize_money, to_decimal


def allocate_shares(
    pool: Decimal,
    weights: list[int],
    rounding: bool = True,
) -> list[Decimal]:
    total_weight = sum(weights)
    if total_weight <= 0:
        return [Decimal("0") for _ in weights]

    pool_decimal = to_decimal(pool)
    raw_shares = []
    for weight in weights:
        if weight <= 0:
            raw_shares.append(Decimal("0"))
        else:
            raw_shares.append((to_decimal(weight) / to_decimal(total_weight)) * pool_decimal)

    if not rounding:
        return raw_shares

    rounded = [quantize_money(value) for value in raw_shares]
    pool_rounded = quantize_money(pool_decimal)
    diff = pool_rounded - sum(rounded)
    if diff == 0:
        return rounded

    step = MONEY_QUANT
    steps = int((abs(diff) / step).to_integral_value(rounding=ROUND_HALF_UP))
    candidates = [idx for idx, weight in enumerate(weights) if weight > 0]
    if not candidates:
        return rounded

    remainders = [raw - rounded[idx] for idx, raw in enumerate(raw_shares)]

    if diff > 0:
        ordered = sorted(candidates, key=lambda idx: (remainders[idx], -idx), reverse=True)
        increment = step
    else:
        ordered = sorted(candidates, key=lambda idx: (remainders[idx], -idx))
        increment = -step

    for i in range(steps):
        idx = ordered[i % len(ordered)]
        next_value = rounded[idx] + increment
        if next_value < 0:
            continue
        rounded[idx] = next_value

    return rounded
