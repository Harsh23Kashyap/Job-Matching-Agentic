import BackgroundOrnaments from "./BackgroundOrnaments.jsx";

export default function EmptyStatePanel({ patternVariant, className = "", children }) {
  return (
    <section className={`portal-panel portal-panel--elevated portal-panel--empty ${className}`.trim()}>
      {patternVariant && <BackgroundOrnaments variant={patternVariant} scope="panel" />}
      {children}
    </section>
  );
}
