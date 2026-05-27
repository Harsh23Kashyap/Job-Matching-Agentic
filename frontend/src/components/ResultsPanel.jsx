import BackgroundOrnaments from "./BackgroundOrnaments.jsx";

export default function ResultsPanel({ backgroundVariant = "jobs", className = "", children }) {
  return (
    <section className={`portal-panel portal-panel--elevated portal-results-panel ${className}`.trim()}>
      <BackgroundOrnaments variant={backgroundVariant} scope="panel" />
      {children}
    </section>
  );
}
