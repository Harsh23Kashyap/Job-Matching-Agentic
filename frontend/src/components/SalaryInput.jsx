import { useEffect, useState } from "react";
import { formatInr, parseInr } from "../utils/format.js";

export default function SalaryInput({ id, value, onChange, error }) {
  const [display, setDisplay] = useState(() => (value ? formatInr(value).replace("₹ ", "") : ""));

  useEffect(() => {
    setDisplay(value ? formatInr(value).replace("₹ ", "") : "");
  }, [value]);

  const handleBlur = () => {
    const parsed = parseInr(display);
    onChange(parsed);
    setDisplay(parsed ? formatInr(parsed).replace("₹ ", "") : "");
  };

  return (
    <div className={`salary-input-wrap${error ? " has-error" : ""}`}>
      <span className="salary-prefix" aria-hidden="true">
        ₹
      </span>
      <input
        id={id}
        type="text"
        inputMode="numeric"
        className="salary-input input-no-spinner"
        placeholder="12,00,000"
        value={display}
        onChange={(e) => setDisplay(e.target.value.replace(/[^\d,]/g, ""))}
        onBlur={handleBlur}
      />
      <span className="salary-suffix">/ year</span>
    </div>
  );
}
