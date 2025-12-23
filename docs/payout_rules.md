# Payout Rules

## Deterministic rounding and allocation

- Pools are quantized to cents before allocation.
- Shares are rounded to cents and adjusted to exactly match the pool total.
- Adjustment uses a largest-remainder pass so the sum equals the pool exactly.
- Validation asserts pool totals match within USD 0.01 tolerance.
