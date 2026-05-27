export default function FormField({ label, helper, error, htmlFor, children }) {
  return (
    <label className="form-field" htmlFor={htmlFor}>
      <span className="form-field-label field-label">{label}</span>
      {helper && <span className="field-helper">{helper}</span>}
      {children}
      {error && <span className="field-error">{error}</span>}
    </label>
  );
}
