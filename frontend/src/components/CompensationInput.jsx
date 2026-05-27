import { useEffect, useState } from "react";
import {
  CURRENCIES,
  filterAmountInput,
  formatAmount,
  formatCompensationPreview,
  parseAmount,
} from "../utils/format.js";

export default function CompensationInput({
  id,
  amount,
  currency = "INR",
  onAmountChange,
  onCurrencyChange,
  error,
}) {
  const [display, setDisplay] = useState(() => (amount ? formatAmount(amount, currency) : ""));

  useEffect(() => {
    setDisplay(amount ? formatAmount(amount, currency) : "");
  }, [amount, currency]);

  const handleChange = (event) => {
    setDisplay(filterAmountInput(event.target.value));
  };

  const handleBlur = () => {
    const parsed = parseAmount(display);
    onAmountChange(parsed);
    setDisplay(parsed ? formatAmount(parsed, currency) : "");
  };

  const preview = formatCompensationPreview(amount, currency);

  return (
    <div className={`compensation-input${error ? " has-error" : ""}`}>
      <div className="compensation-input-row">
        <select
          id={`${id}-currency`}
          className="compensation-currency"
          value={currency}
          onChange={(e) => onCurrencyChange(e.target.value)}
          aria-label="Currency"
        >
          {CURRENCIES.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
        <input
          id={id}
          type="text"
          inputMode="numeric"
          autoComplete="off"
          className="compensation-amount input-no-spinner"
          placeholder={currency === "INR" ? "12,00,000" : "120,000"}
          value={display}
          onChange={handleChange}
          onBlur={handleBlur}
          aria-label="Expected annual total compensation"
          aria-invalid={Boolean(error)}
        />
        <span className="compensation-suffix">per year</span>
      </div>
      {preview && <p className="compensation-preview">{preview}</p>}
    </div>
  );
}
