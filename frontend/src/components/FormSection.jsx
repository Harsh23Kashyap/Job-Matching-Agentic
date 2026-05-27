export default function FormSection({ title, helper, children, className = "" }) {
  return (
    <div className={`portal-form-section ${className}`.trim()}>
      {title && <h3 className="portal-form-section-title">{title}</h3>}
      {helper && <p className="portal-form-section-helper">{helper}</p>}
      {children}
    </div>
  );
}
