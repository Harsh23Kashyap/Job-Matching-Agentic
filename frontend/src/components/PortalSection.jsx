export default function PortalSection({
  title,
  description,
  action,
  children,
  className = "",
  span = 12,
  id,
}) {
  return (
    <section
      id={id}
      className={`portal-panel portal-section span-${span} ${className}`.trim()}
    >
      {(title || action) && (
        <header className="portal-section-head">
          <div className="portal-section-head-text">
            {title && <h2>{title}</h2>}
            {description && <p>{description}</p>}
          </div>
          {action && <div className="portal-section-head-action">{action}</div>}
        </header>
      )}
      <div className="portal-section-body">{children}</div>
    </section>
  );
}
