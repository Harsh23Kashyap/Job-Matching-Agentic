export function Logo({ size = 32 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 40 40" fill="none" aria-hidden="true" className="logo-mark">
      <rect width="40" height="40" rx="11" fill="#FFFCF8" stroke="#E3DBD1" strokeWidth="1" />
      <circle cx="32" cy="8" r="3" fill="#6E8B74" opacity="0.7" />
      <circle cx="14" cy="22" r="3" stroke="#52635A" strokeWidth="1" fill="none" opacity="0.5" />
      <circle cx="26" cy="28" r="3" stroke="#52635A" strokeWidth="1" fill="none" opacity="0.5" />
      <path d="M14 22 L20 18 L26 28" stroke="#52635A" strokeWidth="0.75" opacity="0.35" strokeLinecap="round" />
      <text
        x="20"
        y="17"
        textAnchor="middle"
        fill="#52635A"
        fontSize="9"
        fontWeight="600"
        fontFamily="DM Sans, sans-serif"
        opacity="0.85"
      >
        JM
      </text>
    </svg>
  );
}

export function IconCheck({ size = 14 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M5 12l5 5L19 7" />
    </svg>
  );
}

export function IconBriefcase({ size = 20 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="7" width="20" height="14" rx="2" />
      <path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2" />
      <path d="M2 12h20" />
    </svg>
  );
}

export function IconProfile({ size = 20 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="8" r="4" />
      <path d="M4 21c0-4 3.6-7 8-7s8 3 8 7" />
    </svg>
  );
}

export function IconUpload({ size = 20 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 16V4M12 4l4 4M12 4L8 8" />
      <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2" />
    </svg>
  );
}

export function IconSearch({ size = 20 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="11" cy="11" r="7" />
      <path d="M20 20l-3-3" />
    </svg>
  );
}

export function IconConsole({ size = 20 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="4" width="18" height="14" rx="2" />
      <path d="M8 20h8M12 18v2" />
      <path d="M7 9h10M7 12h6" />
    </svg>
  );
}

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

export function IconRefresh({ size = 18 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M21 12a9 9 0 1 1-2.64-6.36" />
      <path d="M21 3v6h-6" />
    </svg>
  );
}

export function IconCopy({ size = 16 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="9" y="9" width="13" height="13" rx="2" />
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
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
      <rect x="8" y="12" width="104" height="56" rx="6" stroke="#6E8B74" strokeWidth="1.5" opacity="0.25" />
      <line x1="8" y1="28" x2="112" y2="28" stroke="#E3DBD1" strokeWidth="1" />
      <rect x="18" y="38" width="40" height="6" rx="2" fill="#6E8B74" opacity="0.15" />
      <rect x="18" y="50" width="64" height="4" rx="2" fill="#5F7668" opacity="0.15" />
      <circle cx="92" cy="52" r="10" stroke="#5F7668" strokeWidth="1.5" opacity="0.4" />
      <path d="M88 52l3 3 6-6" stroke="#248A3D" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" opacity="0.6" />
    </svg>
  );
}

export function SystemDiagram() {
  return (
    <svg viewBox="0 0 200 48" width="200" height="48" fill="none" aria-hidden="true" className="header-diagram">
      <rect x="4" y="14" width="44" height="20" rx="4" stroke="#6E8B74" strokeWidth="1.2" fill="#6E8B74" fillOpacity="0.06" />
      <text x="26" y="27" textAnchor="middle" fill="#66707A" fontSize="7" fontFamily="DM Sans, sans-serif">UI</text>
      <rect x="78" y="14" width="44" height="20" rx="4" stroke="#5F7668" strokeWidth="1.2" fill="#5F7668" fillOpacity="0.06" />
      <text x="100" y="27" textAnchor="middle" fill="#66707A" fontSize="7" fontFamily="DM Sans, sans-serif">API</text>
      <rect x="152" y="14" width="44" height="20" rx="4" stroke="#5B6472" strokeWidth="1.2" fill="#5B6472" fillOpacity="0.06" />
      <text x="174" y="27" textAnchor="middle" fill="#66707A" fontSize="7" fontFamily="DM Sans, sans-serif">Agents</text>
      <line x1="48" y1="24" x2="78" y2="24" stroke="#E3DBD1" strokeWidth="1" />
      <line x1="122" y1="24" x2="152" y2="24" stroke="#E3DBD1" strokeWidth="1" />
      <circle cx="63" cy="24" r="2" fill="#6E8B74">
        <animate attributeName="opacity" values="1;0.3;1" dur="3s" repeatCount="indefinite" />
      </circle>
      <circle cx="137" cy="24" r="2" fill="#5F7668">
        <animate attributeName="opacity" values="0.3;1;0.3" dur="3s" repeatCount="indefinite" />
      </circle>
    </svg>
  );
}
