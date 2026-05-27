export default function ProfileFormFooter({ dirty, statusText, children }) {
  return (
    <div className="form-footer portal-form-footer">
      <div className="form-footer-inner form-footer-inner--wide">
        <span className={`portal-form-footer__status${dirty ? " portal-form-footer__status--dirty" : ""}`}>
          {statusText ?? (dirty ? "Unsaved changes" : "No changes yet")}
        </span>
        <div className="portal-form-footer__actions">{children}</div>
      </div>
    </div>
  );
}
