export default function PageHeader({ eyebrow, title, subtitle, stats, children, inlineAction }) {
  return (
    <header className="page-hero">
      <div className="page-hero-text">
        {eyebrow && <p className="page-hero-eyebrow">{eyebrow}</p>}
        <h1>{title}</h1>
        {subtitle && <p className="page-hero-subtitle">{subtitle}</p>}
        {stats?.length > 0 && (
          <dl className="page-hero-stats">
            {stats.map((stat) => (
              <div key={stat.label} className="page-hero-stat">
                <dt>{stat.label}</dt>
                <dd>{stat.value}</dd>
              </div>
            ))}
          </dl>
        )}
        {inlineAction && <div className="page-hero-inline">{inlineAction}</div>}
      </div>
      {children && <div className="page-hero-actions">{children}</div>}
    </header>
  );
}
