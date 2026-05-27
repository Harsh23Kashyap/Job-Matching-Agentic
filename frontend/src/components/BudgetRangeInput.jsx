import { useEffect, useState } from "react";
import { CURRENCIES, filterAmountInput, formatAmount, parseAmount } from "../utils/format.js";

function AmountField({ id, label, amount, currency, onChange, placeholder }) {
  const [display, setDisplay] = useState(() => (amount ? formatAmount(amount, currency) : ""));

  useEffect(() => {
    setDisplay(amount ? formatAmount(amount, currency) : "");
  }, [amount, currency]);

  return (
    <div className="budget-range-amount">
      <label className="budget-range-amount-label" htmlFor={id}>
        {label}
      </label>
      <div className="budget-range-amount-row">
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
        <span className="compensation-suffix">per year</span>
      </div>
    </div>
  );
}

export default function BudgetRangeInput({
  currency = "INR",
  minAmount,
  maxAmount,
  onCurrencyChange,
  onMinChange,
  onMaxChange,
  minError,
  maxError,
}) {
  const placeholder = currency === "INR" ? "12,00,000" : "120,000";

  return (
    <div className={`budget-range-input${minError || maxError ? " has-error" : ""}`}>
      <div className="budget-range-currency-row">
        <label className="budget-range-currency-label" htmlFor="job-budget-currency">
          Currency
        </label>
        <select
          id="job-budget-currency"
          className="compensation-currency"
          value={currency}
          onChange={(e) => onCurrencyChange(e.target.value)}
        >
          {CURRENCIES.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>
      <div className="budget-range-amounts">
        <AmountField
          id="job-budget-min"
          label="Min budget"
          amount={minAmount}
          currency={currency}
          onChange={onMinChange}
          placeholder={placeholder}
        />
        <AmountField
          id="job-budget-max"
          label="Max budget"
          amount={maxAmount}
          currency={currency}
          onChange={onMaxChange}
          placeholder={placeholder}
        />
      </div>
      {(minError || maxError) && (
        <p className="field-error" role="alert">
          {minError || maxError}
        </p>
      )}
    </div>
  );
}
