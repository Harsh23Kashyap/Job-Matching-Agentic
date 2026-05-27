export default function CustomCheckbox({ id, checked, onChange, label, helper }) {
  return (
    <label className={`custom-checkbox${checked ? " custom-checkbox--checked" : ""}`} htmlFor={id}>
      <input
        id={id}
        type="checkbox"
        className="custom-checkbox-input"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
      />
      <span className="custom-checkbox-box" aria-hidden="true">
        {checked && "✓"}
      </span>
      <span className="custom-checkbox-text">
        <strong>{label}</strong>
        {helper && <small className="field-helper">{helper}</small>}
      </span>
    </label>
  );
}
