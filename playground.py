"""Small, deliberately optimisable functions using fictional order data."""

import random
import re
from collections import Counter


def sample_orders(count: int, seed: int = 42) -> list[dict]:
    """Return repeatable synthetic data; no real people or transactions."""
    rng = random.Random(seed)
    products = ("coffee", "tea", "toast", "cake", "juice")
    return [
        {
            "customer": f"customer-{rng.randrange(100):03d}",
            "product": rng.choice(products),
            "quantity": rng.randint(1, 5),
            "unit_price_cents": rng.randint(150, 1200),
        }
        for _ in range(count)
    ]


def totals_by_customer(orders: list[dict]) -> dict[str, int]:
    """Correct but intentionally slow: scans all orders for each customer.

    This is the main optimisation exercise. Preserve integer-cent arithmetic
    and output correctness while reducing repeated work.
    """
    customers = sorted({order["customer"] for order in orders})
    return {
        customer: sum(
            order["quantity"] * order["unit_price_cents"]
            for order in orders
            if order["customer"] == customer
        )
        for customer in customers
    }


def top_products(orders: list[dict], limit: int = 3) -> list[tuple[str, int]]:
    """Rank products by quantity, resolving equal counts alphabetically."""
    counts = Counter()
    for order in orders:
        counts[order["product"]] += order["quantity"]
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:max(0, limit)]


def normalize_labels(labels: list[str]) -> list[str]:
    """Normalize whitespace/case and preserve first-occurrence order."""
    result = []
    seen = set()
    for label in labels:
        cleaned = re.sub(r"\s+", " ", label.strip()).casefold()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            result.append(cleaned)
    return result
