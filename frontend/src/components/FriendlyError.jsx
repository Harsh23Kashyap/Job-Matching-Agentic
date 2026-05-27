import { useState } from "react";
import { parseAdminError } from "../utils/adminErrors.js";

export default function FriendlyError({ message, className = "" }) {
  const [open, setOpen] = useState(false);
  if (!message) return null;

  const parsed = parseAdminError(message);

  return (
    <div className={`admin-friendly-error admin-friendly-error--${parsed.severity} ${className}`.trim()} role="alert">
      <p className="admin-friendly-error__title">{parsed.title}</p>
      <p className="admin-friendly-error__summary">{parsed.summary}</p>
      {parsed.details && (
        <div className="admin-friendly-error__details-wrap">
          <button type="button" className="admin-friendly-error__toggle" onClick={() => setOpen((v) => !v)}>
            {open ? "Hide details" : "View details"}
          </button>
          {open && <pre className="admin-friendly-error__details">{parsed.details}</pre>}
        </div>
      )}
    </div>
  );
}
