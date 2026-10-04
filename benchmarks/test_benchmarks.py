"""Keep fixture generation and correctness checks outside measured functions."""

import pytest

from playground import normalize_labels, sample_orders, top_products, totals_by_customer


@pytest.fixture(params=[200, 2000], ids=["small", "large"])
def orders(request):
    return sample_orders(request.param)


def test_customer_totals(benchmark, orders):
    result = benchmark(totals_by_customer, orders)
    assert sum(result.values()) == sum(o["quantity"] * o["unit_price_cents"] for o in orders)


def test_product_ranking(benchmark, orders):
    result = benchmark(top_products, orders)
    assert 0 < len(result) <= 3


@pytest.mark.parametrize("size", [200, 2000], ids=["small", "large"])
def test_label_normalization(benchmark, size):
    labels = [f"  SAMPLE   label {i % 40}  " for i in range(size)]
    result = benchmark(normalize_labels, labels)
    assert result == [f"sample label {i}" for i in range(40)]
