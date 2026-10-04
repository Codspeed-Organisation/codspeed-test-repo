"""Keep fixture generation and correctness checks outside measured functions."""

from collections import Counter

import pytest

from playground import normalize_labels, sample_orders, top_products, totals_by_customer


@pytest.fixture(params=[200, 2000], ids=["small", "large"])
def orders(request):
    return sample_orders(request.param)


def test_customer_totals(benchmark, orders):
    result = benchmark(totals_by_customer, orders)
    expected = {}
    for order in orders:
        customer = order["customer"]
        expected[customer] = expected.get(customer, 0) + order["quantity"] * order["unit_price_cents"]

    assert result == expected


def test_product_ranking(benchmark, orders):
    result = benchmark(top_products, orders)
    product_counts = Counter()
    for order in orders:
        product_counts[order["product"]] += order["quantity"]
    expected = sorted(product_counts.items(), key=lambda item: (-item[1], item[0]))[:3]

    assert result == expected


@pytest.mark.parametrize("size", [200, 2000], ids=["small", "large"])
def test_label_normalization(benchmark, size):
    labels = [f"  SAMPLE   label {i % 40}  " for i in range(size)]
    result = benchmark(normalize_labels, labels)
    assert result == [f"sample label {i}" for i in range(40)]
