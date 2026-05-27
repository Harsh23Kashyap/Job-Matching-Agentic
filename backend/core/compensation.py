"""Normalize compensation fields from API payloads."""
from __future__ import annotations

import re

ALLOWED_CURRENCIES = frozenset({"INR", "USD", "EUR", "GBP", "SGD"})


def normalize_preferred_salary(raw_value) -> int | None:
    if raw_value is None or raw_value == "":
        return None
    if isinstance(raw_value, str):
        stripped = raw_value.strip()
        if not stripped:
            return None
        if "." in stripped:
            try:
                amount = int(round(float(stripped.replace(",", ""))))
            except ValueError:
                return None
        else:
            digits = re.sub(r"[^\d]", "", stripped)
            if not digits:
                return None
            amount = int(digits)
    else:
        try:
            amount = int(round(float(raw_value)))
        except (TypeError, ValueError):
            return None
    return amount if amount > 0 else None


def normalize_preferred_currency(raw_value) -> str:
    currency = str(raw_value or "INR").upper().strip()
    return currency if currency in ALLOWED_CURRENCIES else "INR"
