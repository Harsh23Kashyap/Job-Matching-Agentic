import pytest

from core.compensation import normalize_preferred_currency, normalize_preferred_salary


@pytest.mark.parametrize(
    "raw, expected",
    [
        (None, None),
        ("", None),
        (0, None),
        (-5000, None),
        (1200000, 1200000),
        ("12,00,000", 1200000),
        ("1200000.75", 1200001),
        ("abc", None),
    ],
)
def test_normalize_preferred_salary(raw, expected):
    assert normalize_preferred_salary(raw) == expected


@pytest.mark.parametrize(
    "raw, expected",
    [
        (None, "INR"),
        ("", "INR"),
        ("inr", "INR"),
        ("USD", "USD"),
        ("eur", "EUR"),
        ("JPY", "INR"),
        ("  gbp ", "GBP"),
    ],
)
def test_normalize_preferred_currency(raw, expected):
    assert normalize_preferred_currency(raw) == expected
