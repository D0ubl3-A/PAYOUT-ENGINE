from decimal import Decimal
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.allocation import allocate_shares


def test_allocate_shares_rounding_upward_adjustment() -> None:
    pool = Decimal("100.00")
    weights = [1, 1, 1]
    shares = allocate_shares(pool, weights, rounding=True)
    assert sum(shares) == pool
    assert shares.count(Decimal("33.33")) == 2
    assert shares.count(Decimal("33.34")) == 1


def test_allocate_shares_rounding_downward_adjustment() -> None:
    pool = Decimal("100.01")
    weights = [1, 1, 1]
    shares = allocate_shares(pool, weights, rounding=True)
    assert sum(shares) == Decimal("100.01")
    assert shares.count(Decimal("33.34")) == 2
    assert shares.count(Decimal("33.33")) == 1
