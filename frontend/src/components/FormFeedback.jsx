import { IconAlert } from "./icons.jsx";

const VARIANTS = {
  error: "form-feedback--error",
  success: "form-feedback--success",
  info: "form-feedback--info",
};

export default function FormFeedback({ variant = "info", title, message, children }) {
  if (!title && !message && !children) return null;

  return (
    <div className={`form-feedback ${VARIANTS[variant] || VARIANTS.info}`} role={variant === "error" ? "alert" : "status"}>
      {variant === "error" && (
        <span className="form-feedback__icon" aria-hidden="true">
          <IconAlert size={18} />
        </span>
      )}
      <div className="form-feedback__body">
        {title && <p className="form-feedback__title">{title}</p>}
        {message && <p className="form-feedback__message">{message}</p>}
        {children}
      </div>
    </div>
  );
}
