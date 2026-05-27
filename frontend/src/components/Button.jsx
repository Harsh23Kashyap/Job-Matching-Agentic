export default function Button({ children, loading, loadingLabel, className = "btn-primary", ...props }) {
  return (
    <button type="button" className={`${className}${loading ? " btn-loading" : ""}`} disabled={loading || props.disabled} {...props}>
      {loading && <span className="btn-spinner" aria-hidden="true" />}
      {loading ? loadingLabel || children : children}
    </button>
  );
}
