/** Decorative SVGs for auth pages — sage/charcoal/sand, thin strokes, low opacity. */

export function AuthBlobs() {
  return (
    <div className="auth-blobs" aria-hidden="true">
      <svg className="auth-blob auth-blob--sand-lg" viewBox="0 0 400 400" fill="none">
        <path
          d="M280 320c-60 80-180 60-200-20C60 220 100 80 200 60c120-24 200 100 80 260z"
          fill="#E5D8C7"
          opacity="0.5"
        />
      </svg>
      <svg className="auth-blob auth-blob--sand-sm" viewBox="0 0 120 120" fill="none">
        <path
          d="M60 10c30 0 55 28 50 58-5 35-45 52-70 30C15 75 20 25 60 10z"
          fill="#D7C8B4"
          opacity="0.45"
        />
      </svg>
      <svg className="auth-blob auth-blob--sage" viewBox="0 0 80 80" fill="none">
        <circle cx="40" cy="40" r="32" fill="#C8D2C3" opacity="0.4" />
      </svg>
      <svg className="auth-blob auth-blob--outline" viewBox="0 0 160 160" fill="none">
        <path
          d="M80 20c40 0 70 35 65 72-5 42-50 68-85 45C25 115 15 55 80 20z"
          stroke="#8A9A8C"
          strokeWidth="1"
          fill="none"
          opacity="0.2"
        />
      </svg>
    </div>
  );
}

export function AuthMiniCards() {
  return (
    <div className="auth-mini-cards" aria-hidden="true">
      <span>Skill match</span>
      <span>Resume parsed</span>
      <span>Role fit</span>
    </div>
  );
}

export function AuthMatchingScene() {
  return (
    <div className="auth-matching-scene left-visual" aria-hidden="true">
      <svg className="auth-scene-connectors" viewBox="0 0 420 220" fill="none">
        <path
          d="M95 110 Q160 60 210 95"
          stroke="#8A9A8C"
          strokeWidth="1"
          opacity="0.25"
          strokeDasharray="4 6"
        />
        <path
          d="M210 95 Q270 130 320 100"
          stroke="#8A9A8C"
          strokeWidth="1"
          opacity="0.25"
        />
        <path
          d="M95 110 Q155 160 210 95"
          stroke="#8A9A8C"
          strokeWidth="1"
          opacity="0.2"
        />
        <circle cx="210" cy="95" r="14" stroke="#52635A" strokeWidth="1" fill="#E8EFE8" opacity="0.6" />
        <circle cx="210" cy="95" r="4" fill="#52635A" opacity="0.45" />
        <circle cx="95" cy="110" r="5" fill="#8A9A8C" opacity="0.3" />
        <circle cx="320" cy="100" r="5" fill="#8A9A8C" opacity="0.3" />
      </svg>

      {/* Resume card */}
      <svg className="auth-scene-resume" viewBox="0 0 140 120" fill="none">
        <rect x="8" y="8" width="124" height="104" rx="12" fill="rgba(255,252,248,0.75)" stroke="#8A9A8C" strokeWidth="1" opacity="0.7" />
        <circle cx="36" cy="38" r="14" stroke="#52635A" strokeWidth="1" opacity="0.4" />
        <path d="M28 38h16M36 30v16" stroke="#52635A" strokeWidth="0.75" opacity="0.25" />
        <line x1="58" y1="32" x2="110" y2="32" stroke="#8A9A8C" strokeWidth="1.5" opacity="0.35" strokeLinecap="round" />
        <line x1="58" y1="44" x2="96" y2="44" stroke="#8A9A8C" strokeWidth="1" opacity="0.25" strokeLinecap="round" />
        <line x1="24" y1="68" x2="116" y2="68" stroke="#DCCDB8" strokeWidth="1" opacity="0.4" />
        <line x1="24" y1="80" x2="100" y2="80" stroke="#DCCDB8" strokeWidth="1" opacity="0.3" strokeLinecap="round" />
        <line x1="24" y1="92" x2="108" y2="92" stroke="#DCCDB8" strokeWidth="1" opacity="0.25" strokeLinecap="round" />
      </svg>

      {/* Floating job card */}
      <div className="auth-scene-job-card">
        <div className="auth-job-card-header">
          <span className="auth-job-card-title">Backend Engineer</span>
          <span className="auth-job-card-score">92%</span>
        </div>
        <span className="auth-job-card-company">Northbridge Labs · Remote</span>
        <div className="auth-job-card-chips">
          <span>Python</span>
          <span>Swift</span>
          <span>ML</span>
        </div>
      </div>

      {/* Employer card (small, line art) */}
      <svg className="auth-scene-employer" viewBox="0 0 100 72" fill="none">
        <rect x="4" y="4" width="92" height="64" rx="10" fill="rgba(255,252,248,0.5)" stroke="#8A9A8C" strokeWidth="1" opacity="0.4" />
        <rect x="16" y="18" width="24" height="24" rx="6" stroke="#52635A" strokeWidth="1" opacity="0.35" />
        <line x1="48" y1="22" x2="80" y2="22" stroke="#8A9A8C" strokeWidth="1.5" opacity="0.3" strokeLinecap="round" />
        <line x1="48" y1="34" x2="68" y2="34" stroke="#8A9A8C" strokeWidth="1" opacity="0.25" strokeLinecap="round" />
        <line x1="16" y1="52" x2="84" y2="52" stroke="#DCCDB8" strokeWidth="1" opacity="0.35" />
      </svg>
    </div>
  );
}

export function AuthRightDecor() {
  return (
    <div className="auth-right-decor" aria-hidden="true">
      <svg className="auth-contour auth-contour--connections" viewBox="0 0 600 800" fill="none">
        <path d="M480 120 Q360 200 420 340" stroke="#52635A" strokeWidth="1" opacity="0.08" />
        <path d="M520 280 Q400 360 440 520" stroke="#52635A" strokeWidth="1" opacity="0.08" />
        <path d="M560 440 Q480 500 500 640" stroke="#52635A" strokeWidth="1" opacity="0.06" />
        <circle cx="480" cy="120" r="4" fill="#52635A" opacity="0.08" />
        <circle cx="420" cy="340" r="4" fill="#52635A" opacity="0.08" />
        <circle cx="440" cy="520" r="4" fill="#52635A" opacity="0.06" />
      </svg>
      <svg className="auth-contour auth-contour--tr" viewBox="0 0 320 240" fill="none">
        <path
          d="M20 200 Q80 160 120 180 T220 140 T300 100"
          stroke="#8A9A8C"
          strokeWidth="1"
          opacity="0.12"
          fill="none"
        />
        <path
          d="M40 220 Q100 190 160 200 T280 160"
          stroke="#8A9A8C"
          strokeWidth="1"
          opacity="0.08"
          fill="none"
        />
        <ellipse cx="260" cy="60" rx="80" ry="50" fill="#E5D8C7" opacity="0.25" />
      </svg>
      <svg className="auth-contour auth-contour--br" viewBox="0 0 200 160" fill="none">
        <path
          d="M10 140c40-30 90-20 120 10s60 20 70-10"
          stroke="#8A9A8C"
          strokeWidth="1"
          opacity="0.1"
        />
        <circle cx="160" cy="120" r="48" fill="#D7C8B4" opacity="0.2" />
      </svg>
    </div>
  );
}

export function AuthDividerShadow() {
  return <div className="auth-panel-divider" aria-hidden="true" />;
}
