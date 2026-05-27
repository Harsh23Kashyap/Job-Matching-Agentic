/** Decorative SVGs for auth — token-driven strokes, low density. */

export function AuthBlobs() {
  return (
    <div className="auth-blobs" aria-hidden="true">
      <svg className="auth-blob auth-blob--sand-lg" viewBox="0 0 400 400" fill="none">
        <path
          d="M280 320c-60 80-180 60-200-20C60 220 100 80 200 60c120-24 200 100 80 260z"
          fill="var(--auth-blob-fill-1)"
          opacity="0.55"
        />
      </svg>
      <svg className="auth-blob auth-blob--sage" viewBox="0 0 80 80" fill="none">
        <circle cx="40" cy="40" r="32" fill="var(--auth-blob-fill-3)" opacity="0.45" />
      </svg>
      <svg className="auth-blob auth-blob--outline" viewBox="0 0 160 160" fill="none">
        <path
          d="M80 20c40 0 70 35 65 72-5 42-50 68-85 45C25 115 15 55 80 20z"
          stroke="var(--auth-illustration-stroke)"
          strokeWidth="1"
          fill="none"
          opacity="0.35"
        />
      </svg>
    </div>
  );
}

export function AuthMiniCards() {
  return (
    <div className="auth-mini-cards" aria-hidden="true">
      <span>Skills</span>
      <span>Experience</span>
      <span>Fit score</span>
    </div>
  );
}

export function AuthMatchingScene() {
  return (
    <div className="auth-matching-scene left-visual" aria-hidden="true">
      <svg className="auth-scene-connectors" viewBox="0 0 320 180" fill="none">
        <path
          d="M88 100 Q140 55 168 88"
          stroke="var(--auth-illustration-stroke)"
          strokeWidth="1"
          opacity="0.22"
          strokeDasharray="4 6"
        />
        <path
          d="M168 88 Q220 115 268 92"
          stroke="var(--auth-illustration-stroke)"
          strokeWidth="1"
          opacity="0.2"
        />
        <circle cx="168" cy="88" r="12" stroke="var(--auth-illustration-accent)" strokeWidth="1" fill="var(--auth-illustration-soft)" opacity="0.55" />
        <circle cx="88" cy="100" r="4" fill="var(--auth-illustration-stroke)" opacity="0.28" />
        <circle cx="268" cy="92" r="4" fill="var(--auth-illustration-stroke)" opacity="0.28" />
      </svg>

      <svg className="auth-scene-resume" viewBox="0 0 120 104" fill="none">
        <rect
          x="6"
          y="6"
          width="108"
          height="92"
          rx="10"
          fill="var(--auth-scene-card-bg)"
          stroke="var(--auth-illustration-stroke)"
          strokeWidth="1"
          opacity="0.75"
        />
        <circle cx="32" cy="34" r="12" stroke="var(--auth-illustration-accent)" strokeWidth="1" opacity="0.4" />
        <line x1="52" y1="28" x2="98" y2="28" stroke="var(--auth-illustration-stroke)" strokeWidth="1.5" opacity="0.32" strokeLinecap="round" />
        <line x1="52" y1="40" x2="84" y2="40" stroke="var(--auth-illustration-stroke)" strokeWidth="1" opacity="0.24" strokeLinecap="round" />
        <line x1="20" y1="58" x2="100" y2="58" stroke="var(--auth-illustration-stroke)" strokeWidth="1" opacity="0.18" />
        <line x1="20" y1="70" x2="88" y2="70" stroke="var(--auth-illustration-stroke)" strokeWidth="1" opacity="0.14" strokeLinecap="round" />
      </svg>

      <div className="auth-scene-job-card">
        <div className="auth-job-card-header">
          <span className="auth-job-card-title">Backend Engineer</span>
          <span className="auth-job-card-score">92%</span>
        </div>
        <span className="auth-job-card-company">Northbridge Labs · Remote</span>
        <div className="auth-job-card-chips">
          <span>Python</span>
          <span>APIs</span>
        </div>
      </div>
    </div>
  );
}

export function AuthRightDecor() {
  return (
    <div className="auth-right-decor" aria-hidden="true">
      <svg className="auth-contour auth-contour--connections" viewBox="0 0 600 800" fill="none">
        <path d="M480 120 Q360 200 420 340" stroke="var(--auth-illustration-accent)" strokeWidth="1" opacity="0.06" />
        <path d="M520 280 Q400 360 440 520" stroke="var(--auth-illustration-accent)" strokeWidth="1" opacity="0.05" />
        <circle cx="480" cy="120" r="3" fill="var(--auth-illustration-accent)" opacity="0.06" />
        <circle cx="420" cy="340" r="3" fill="var(--auth-illustration-accent)" opacity="0.05" />
      </svg>
      <svg className="auth-contour auth-contour--tr" viewBox="0 0 320 240" fill="none">
        <path
          d="M20 200 Q80 160 120 180 T220 140 T300 100"
          stroke="var(--auth-illustration-stroke)"
          strokeWidth="1"
          opacity="0.1"
          fill="none"
        />
        <ellipse cx="260" cy="60" rx="72" ry="44" fill="var(--auth-blob-fill-1)" opacity="0.18" />
      </svg>
    </div>
  );
}

export function AuthDividerShadow() {
  return <div className="auth-panel-divider" aria-hidden="true" />;
}
