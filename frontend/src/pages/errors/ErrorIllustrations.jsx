export function ErrorArtBrokenRoute() {
  return (
    <svg
      viewBox="0 0 180 140"
      width="180"
      height="140"
      fill="none"
      aria-hidden="true"
      className="error-art-svg error-art-svg--broken"
    >
      <rect x="24" y="28" width="58" height="74" rx="10" fill="#f5f0e8" stroke="#ded6ca" strokeWidth="1.5" />
      <rect x="34" y="42" width="38" height="6" rx="3" fill="#e5d8c7" />
      <rect x="34" y="54" width="28" height="5" rx="2.5" fill="#e5d8c7" opacity="0.85" />
      <rect x="34" y="65" width="32" height="5" rx="2.5" fill="#e5d8c7" opacity="0.7" />
      <path d="M82 65h18" stroke="#52635a" strokeWidth="2" strokeLinecap="round" strokeDasharray="3 5" />
      <circle cx="118" cy="65" r="16" fill="#e8efe9" stroke="#52635a" strokeWidth="1.5" />
      <path d="M118 57v9" stroke="#52635a" strokeWidth="2.5" strokeLinecap="round" />
      <circle cx="118" cy="72" r="1.5" fill="#52635a" />
      <circle cx="146" cy="98" r="5" fill="#52635a" opacity="0.25" />
      <circle cx="158" cy="88" r="3" fill="#c9d5cc" opacity="0.5" />
    </svg>
  );
}

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
  return <ErrorArtBrokenRoute />;
}

const ARTS = {
  401: ErrorArt401,
  402: ErrorArt402,
  403: ErrorArt403,
  501: ErrorArt501,
  502: ErrorArt502,
};

export function ErrorIllustration({ code, variant = "default" }) {
  if (variant === "broken") {
    return <ErrorArtBrokenRoute />;
  }
  const Art = ARTS[code] || ErrorArtBrokenRoute;
  return <Art />;
}
