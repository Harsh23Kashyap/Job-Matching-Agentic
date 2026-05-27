import { useState } from "react";

export default function FormAccordionSection({
  title,
  helper,
  children,
  defaultOpen = false,
  badge,
  id,
}) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <section className={`form-accordion${open ? " form-accordion--open" : ""}`} id={id}>
      <button
        type="button"
        className="form-accordion__trigger"
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
      >
        <span className="form-accordion__title-wrap">
          <span className="form-accordion__title">{title}</span>
          {badge ? <span className="form-accordion__badge">{badge}</span> : null}
        </span>
        <span className="form-accordion__chevron" aria-hidden="true">
          {open ? "−" : "+"}
        </span>
      </button>
      {open && (
        <div className="form-accordion__body">
          {helper ? <p className="form-accordion__helper">{helper}</p> : null}
          {children}
        </div>
      )}
    </section>
  );
}
