import { useEffect, useState } from "react";
import {
  CURRENCIES,
  filterAmountInput,
  formatAmount,
  formatCompensationPreview,
  formatCompensationRangePreview,
  parseAmount,
} from "../utils/format.js";

function AmountField({ id, label, amount, currency, onChange, placeholder, suffix = "per year" }) {
  const [display, setDisplay] = useState(() => (amount ? formatAmount(amount, currency) : ""));

  useEffect(() => {
    setDisplay(amount ? formatAmount(amount, currency) : "");
  }, [amount, currency]);

  return (
    <div className="compensation-amount-field">
      {label && (
        <label className="compensation-amount-label" htmlFor={id}>
          {label}
        </label>
      )}
      <div className="compensation-input-row compensation-input-row--amount">
        <input
          id={id}
          type="text"
          inputMode="numeric"
          autoComplete="off"
          className="compensation-amount input-no-spinner"
          placeholder={placeholder}
          value={display}
          onChange={(e) => setDisplay(filterAmountInput(e.target.value))}
          onBlur={() => {
            const parsed = parseAmount(display);
            onChange(parsed);
            setDisplay(parsed ? formatAmount(parsed, currency) : "");
          }}
        />
        <span className="compensation-suffix">{suffix}</span>
      </div>
    </div>
  );
}

/**
 * Shared compensation input for candidate expected salary (single) and employer budget range.
 * @param {"single"|"range"} mode
 */
export default function CompensationInput({
  id = "compensation",
  mode = "single",
  amount,
  minAmount,
  maxAmount,
  currency = "INR",
  onAmountChange,
  onMinChange,
  onMaxChange,
  onCurrencyChange,
  error,
  minError,
  maxError,
}) {
  const [display, setDisplay] = useState(() => (amount ? formatAmount(amount, currency) : ""));

  useEffect(() => {
    if (mode === "single") {
      setDisplay(amount ? formatAmount(amount, currency) : "");
    }
  }, [amount, currency, mode]);

  const placeholder = currency === "INR" ? "12,00,000" : "120,000";
  const hasError = Boolean(error || minError || maxError);
  const preview =
    mode === "single"
      ? formatCompensationPreview(amount, currency)
      : formatCompensationRangePreview(minAmount, maxAmount, currency);

  const handleSingleChange = (event) => {
    setDisplay(filterAmountInput(event.target.value));
  };

  const handleSingleBlur = () => {
    const parsed = parseAmount(display);
    onAmountChange?.(parsed);
    setDisplay(parsed ? formatAmount(parsed, currency) : "");
  };

  return (
    <div className={`compensation-input${hasError ? " has-error" : ""}`}>
      <div className="compensation-currency-row">
        <label className="compensation-currency-label" htmlFor={`${id}-currency`}>
          Currency
        </label>
        <select
          id={`${id}-currency`}
          className="compensation-currency"
          value={currency}
          onChange={(e) => onCurrencyChange?.(e.target.value)}
          aria-label="Currency"
        >
          {CURRENCIES.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      {mode === "single" ? (
        <div className="compensation-input-row">
          <input
            id={id}
            type="text"
            inputMode="numeric"
            autoComplete="off"
            className="compensation-amount input-no-spinner"
            placeholder={placeholder}
            value={display}
            onChange={handleSingleChange}
            onBlur={handleSingleBlur}
            aria-label="Expected annual total compensation"
            aria-invalid={Boolean(error)}
          />
          <span className="compensation-suffix">per year</span>
        </div>
      ) : (
        <div className="compensation-range-amounts">
          <AmountField
            id={`${id}-min`}
            label="Minimum total"
            amount={minAmount}
            currency={currency}
            onChange={onMinChange}
            placeholder={placeholder}
          />
          <AmountField
            id={`${id}-max`}
            label="Maximum total"
            amount={maxAmount}
            currency={currency}
            onChange={onMaxChange}
            placeholder={placeholder}
          />
        </div>
      )}

      {preview && <p className="compensation-preview">{preview}</p>}
      {(error || minError || maxError) && (
        <p className="field-error" role="alert">
          {error || minError || maxError}
        </p>
      )}
    </div>
  );
}
