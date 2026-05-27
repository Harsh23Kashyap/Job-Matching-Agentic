export default function FormField({ label, helper, error, htmlFor, optional, children }) {
  return (
    <div className="form-field">
      <label className="form-field-label field-label" htmlFor={htmlFor}>
        {label}
        {optional && <span className="field-optional">Optional</span>}
      </label>
      {helper && <p className="field-helper">{helper}</p>}
      <div className="form-field-control">{children}</div>
      {error && (
        <p className="field-error" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
