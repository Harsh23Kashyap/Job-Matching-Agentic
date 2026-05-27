export function ErrorArt401() {
  return (
    <svg viewBox="0 0 200 160" fill="none" aria-hidden="true" className="error-art-svg">
      <rect x="40" y="30" width="120" height="90" rx="12" fill="var(--brand-light)" stroke="var(--brand)" strokeWidth="2" />
      <circle cx="100" cy="68" r="18" fill="var(--brand)" opacity="0.15" />
      <path d="M100 58v12M100 78h.01" stroke="var(--brand)" strokeWidth="3" strokeLinecap="round" />
      <rect x="58" y="98" width="84" height="10" rx="5" fill="var(--border)" />
    </svg>
  );
}

export function ErrorArt402() {
  return (
    <svg viewBox="0 0 200 160" fill="none" aria-hidden="true" className="error-art-svg">
      <path d="M100 24l16 32h36l-28 22 10 34-34-22-34 22 10-34-28-22h36z" fill="#F8C77E" stroke="#915907" strokeWidth="1.5" />
      <rect x="55" y="108" width="90" height="28" rx="14" fill="var(--accent-hover)" />
      <rect x="72" y="118" width="56" height="8" rx="4" fill="#fff" opacity="0.9" />
    </svg>
  );
}

export function ErrorArt403() {
  return (
    <svg viewBox="0 0 200 160" fill="none" aria-hidden="true" className="error-art-svg">
      <rect x="70" y="50" width="60" height="70" rx="8" fill="var(--critical)" opacity="0.12" stroke="var(--critical)" strokeWidth="2" />
      <path d="M85 75h30M85 90h30M85 105h18" stroke="var(--critical)" strokeWidth="3" strokeLinecap="round" />
      <circle cx="130" cy="45" r="22" fill="var(--bg-card)" stroke="var(--critical)" strokeWidth="2" />
      <path d="M122 45l16 16M138 45l-16 16" stroke="var(--critical)" strokeWidth="2.5" strokeLinecap="round" />
    </svg>
  );
}

export function ErrorArt501() {
  return (
    <svg viewBox="0 0 200 160" fill="none" aria-hidden="true" className="error-art-svg">
      <rect x="35" y="40" width="130" height="80" rx="10" fill="var(--bg-elevated)" stroke="var(--border)" strokeWidth="2" />
      <path d="M55 65h90M55 85h70M55 105h50" stroke="var(--border)" strokeWidth="6" strokeLinecap="round" />
      <circle cx="145" cy="105" r="28" fill="var(--warning)" opacity="0.2" />
      <text x="145" y="112" textAnchor="middle" fill="var(--warning)" fontSize="22" fontWeight="700" fontFamily="inherit">
        ?
      </text>
    </svg>
  );
}

export function ErrorArt502() {
  return (
    <svg viewBox="0 0 200 160" fill="none" aria-hidden="true" className="error-art-svg">
      <ellipse cx="100" cy="120" rx="70" ry="12" fill="var(--border-subtle)" />
      <rect x="55" y="35" width="90" height="70" rx="8" fill="var(--bg-card)" stroke="var(--border)" strokeWidth="2" />
      <rect x="65" y="48" width="70" height="8" rx="4" fill="var(--healthy)" opacity="0.4" />
      <rect x="65" y="64" width="50" height="8" rx="4" fill="var(--accent)" opacity="0.35" />
      <rect x="65" y="80" width="60" height="8" rx="4" fill="var(--critical)" opacity="0.5" />
      <path d="M145 35l12-12M157 35l-12-12" stroke="var(--critical)" strokeWidth="2.5" strokeLinecap="round" />
      <circle cx="151" cy="29" r="18" fill="none" stroke="var(--critical)" strokeWidth="2" strokeDasharray="4 4" />
    </svg>
  );
}

const ARTS = {
  401: ErrorArt401,
  402: ErrorArt402,
  403: ErrorArt403,
  501: ErrorArt501,
  502: ErrorArt502,
};

export function ErrorIllustration({ code }) {
  const Art = ARTS[code] || ErrorArt502;
  return <Art />;
}
