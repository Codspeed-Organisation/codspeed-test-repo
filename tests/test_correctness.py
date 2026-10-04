import pytest

from playground import normalize_labels, sample_orders, top_products, totals_by_customer


@pytest.fixture
def orders():
    return [
        {"customer": "a", "product": "tea", "quantity": 2, "unit_price_cents": 250},
        {"customer": "b", "product": "toast", "quantity": 3, "unit_price_cents": 400},
        {"customer": "a", "product": "toast", "quantity": 1, "unit_price_cents": 400},
    ]


def test_totals_use_quantity_and_integer_cents(orders):
    assert totals_by_customer(orders) == {"a": 900, "b": 1200}


def test_totals_empty():
    assert totals_by_customer([]) == {}


def test_totals_do_not_mutate_input(orders):
    original = [dict(order) for order in orders]
    totals_by_customer(orders)
    assert orders == original


def test_top_products_counts_units(orders):
    assert top_products(orders) == [("toast", 4), ("tea", 2)]


def test_top_products_limit(orders):
    assert top_products(orders, 1) == [("toast", 4)]
    assert top_products(orders, 0) == []
    assert top_products(orders, -1) == []


def test_top_products_tie_order():
    data = [{"product": "tea", "quantity": 2}, {"product": "coffee", "quantity": 2}]
    assert top_products(data) == [("coffee", 2), ("tea", 2)]


def test_normalization_and_stable_deduplication():
    assert normalize_labels(["  Coffee  SHOP ", "coffee shop", "TEA\tTIME", "", "  ", "Tea Time"]) == ["coffee shop", "tea time"]


def test_unicode_casefold():
    assert normalize_labels(["Straße", "STRASSE"]) == ["strasse"]


def test_synthetic_data_is_repeatable():
    assert sample_orders(20) == sample_orders(20)
    assert sample_orders(0) == []


def test_totals_conserve_full_order_value():
    data = sample_orders(100)
    expected_total = sum(order["quantity"] * order["unit_price_cents"] for order in data)
    assert sum(totals_by_customer(data).values()) == expected_total
