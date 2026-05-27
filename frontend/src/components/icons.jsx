export function IconAgents({ size = 20 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="8" r="3" />
      <path d="M5 20c0-3.3 3.1-6 7-6s7 2.7 7 6" />
      <circle cx="5" cy="10" r="2" />
      <path d="M2 20c0-2.2 1.8-4 3-4" />
      <circle cx="19" cy="10" r="2" />
      <path d="M19 20c2.2 0 3-1.8 3-4" />
    </svg>
  );
}

export function IconMatch({ size = 20 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M16 3h5v5" />
      <path d="M8 21H3v-5" />
      <path d="M21 3l-7 7" />
      <path d="M3 21l7-7" />
    </svg>
  );
}

export function IconResults({ size = 20 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 3v18h18" />
      <path d="M7 14l4-4 4 4 5-6" />
    </svg>
  );
}

export function IconSun({ size = 18 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" aria-hidden="true">
      <circle cx="12" cy="12" r="4" />
      <path d="M12 2v2M12 20v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M2 12h2M20 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
    </svg>
  );
}

export function IconMoon({ size = 18 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" aria-hidden="true">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
    </svg>
  );
}

export function IconAlert({ size = 18 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" aria-hidden="true">
      <circle cx="12" cy="12" r="9" />
      <path d="M12 8v4M12 16h.01" />
    </svg>
  );
}

export function IconEmpty({ size = 48 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 120 80" fill="none" aria-hidden="true">
      <rect x="8" y="12" width="104" height="56" rx="6" stroke="#0071E3" strokeWidth="1.5" opacity="0.25" />
      <line x1="8" y1="28" x2="112" y2="28" stroke="#E2E4EA" strokeWidth="1" />
      <rect x="18" y="38" width="40" height="6" rx="2" fill="#0071E3" opacity="0.15" />
      <rect x="18" y="50" width="64" height="4" rx="2" fill="#248A3D" opacity="0.15" />
      <circle cx="92" cy="52" r="10" stroke="#248A3D" strokeWidth="1.5" opacity="0.4" />
      <path d="M88 52l3 3 6-6" stroke="#248A3D" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" opacity="0.6" />
    </svg>
  );
}

export function SystemDiagram() {
  return (
    <svg viewBox="0 0 200 48" width="200" height="48" fill="none" aria-hidden="true" className="header-diagram">
      <rect x="4" y="14" width="44" height="20" rx="4" stroke="#0071E3" strokeWidth="1.2" fill="#0071E3" fillOpacity="0.06" />
      <text x="26" y="27" textAnchor="middle" fill="#6E6E73" fontSize="7" fontFamily="-apple-system, sans-serif">UI</text>
      <rect x="78" y="14" width="44" height="20" rx="4" stroke="#248A3D" strokeWidth="1.2" fill="#248A3D" fillOpacity="0.06" />
      <text x="100" y="27" textAnchor="middle" fill="#6E6E73" fontSize="7" fontFamily="-apple-system, sans-serif">API</text>
      <rect x="152" y="14" width="44" height="20" rx="4" stroke="#5856D6" strokeWidth="1.2" fill="#5856D6" fillOpacity="0.06" />
      <text x="174" y="27" textAnchor="middle" fill="#6E6E73" fontSize="7" fontFamily="-apple-system, sans-serif">Agents</text>
      <line x1="48" y1="24" x2="78" y2="24" stroke="#D2D2D7" strokeWidth="1" />
      <line x1="122" y1="24" x2="152" y2="24" stroke="#D2D2D7" strokeWidth="1" />
      <circle cx="63" cy="24" r="2" fill="#0071E3">
        <animate attributeName="opacity" values="1;0.3;1" dur="3s" repeatCount="indefinite" />
      </circle>
      <circle cx="137" cy="24" r="2" fill="#248A3D">
        <animate attributeName="opacity" values="0.3;1;0.3" dur="3s" repeatCount="indefinite" />
      </circle>
    </svg>
  );
}
