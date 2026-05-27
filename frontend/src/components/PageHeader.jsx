export default function PageHeader({ title, subtitle, children, inlineAction }) {
  return (
    <header className="page-hero">
      <div className="page-hero-text">
        <h1>{title}</h1>
        {subtitle && <p>{subtitle}</p>}
        {inlineAction && <div className="page-hero-inline">{inlineAction}</div>}
      </div>
      {children && <div className="page-hero-actions">{children}</div>}
    </header>
  );
}
