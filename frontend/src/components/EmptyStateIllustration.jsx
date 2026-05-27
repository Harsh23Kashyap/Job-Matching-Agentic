import { useId } from "react";
import { useReducedMotion } from "../hooks/useReducedMotion.js";

const STROKE = "var(--illustration-stroke)";
const OLIVE = "var(--illustration-accent)";
const SAND = "var(--illustration-sand)";

function ProfileNeededArt({ reducedMotion }) {
  return (
    <svg className="empty-state-illustration" viewBox="0 0 280 160" fill="none" aria-hidden="true">
      <g className={reducedMotion ? undefined : "empty-illustration__float-a"}>
        <rect x="36" y="24" width="88" height="112" rx="10" stroke={STROKE} strokeWidth="1.2" opacity="0.55" />
        <line x1="52" y1="48" x2="108" y2="48" stroke={STROKE} strokeWidth="1" opacity="0.4" />
        <line x1="52" y1="64" x2="96" y2="64" stroke={STROKE} strokeWidth="1" opacity="0.32" />
        <line x1="52" y1="80" x2="88" y2="80" stroke={STROKE} strokeWidth="1" opacity="0.26" />
        <path d="M80 108 V88 M80 88 L72 96 M80 88 L88 96" stroke={OLIVE} strokeWidth="1" strokeLinecap="round" opacity="0.45" />
      </g>
      <g className={reducedMotion ? undefined : "empty-illustration__float-b"}>
        <rect x="156" y="36" width="96" height="88" rx="10" stroke={STROKE} strokeWidth="1.2" opacity="0.5" />
        <circle cx="172" cy="58" r="3" stroke={STROKE} strokeWidth="1" opacity="0.45" />
        <circle cx="172" cy="78" r="3" stroke={STROKE} strokeWidth="1" opacity="0.4" />
        <circle cx="172" cy="98" r="3" stroke={STROKE} strokeWidth="1" opacity="0.35" />
        <line x1="184" y1="58" x2="236" y2="58" stroke={STROKE} strokeWidth="1" opacity="0.32" />
        <line x1="184" y1="78" x2="224" y2="78" stroke={STROKE} strokeWidth="1" opacity="0.28" />
        <line x1="184" y1="98" x2="216" y2="98" stroke={STROKE} strokeWidth="1" opacity="0.24" />
      </g>
    </svg>
  );
}

function ReadyArt({ reducedMotion, pathId }) {
  return (
    <svg className="empty-state-illustration" viewBox="0 0 320 180" fill="none" aria-hidden="true">
      <g className={reducedMotion ? undefined : "empty-illustration__float-a"}>
        <rect x="24" y="88" width="80" height="56" rx="10" stroke={STROKE} strokeWidth="1.2" opacity="0.55" />
        <circle cx="44" cy="108" r="8" stroke={STROKE} strokeWidth="1" opacity="0.4" />
        <line x1="60" y1="104" x2="88" y2="104" stroke={STROKE} strokeWidth="1" opacity="0.32" />
        <line x1="60" y1="118" x2="80" y2="118" stroke={STROKE} strokeWidth="1" opacity="0.26" />
      </g>
      <g className={reducedMotion ? undefined : "empty-illustration__float-b"}>
        <rect x="216" y="88" width="80" height="56" rx="10" stroke={STROKE} strokeWidth="1.2" opacity="0.55" />
        <rect x="232" y="102" width="16" height="16" rx="4" stroke={STROKE} strokeWidth="1" opacity="0.35" />
        <line x1="254" y1="106" x2="280" y2="106" stroke={STROKE} strokeWidth="1" opacity="0.32" />
        <line x1="254" y1="120" x2="272" y2="120" stroke={STROKE} strokeWidth="1" opacity="0.26" />
      </g>
      <path
        id={pathId}
        className={reducedMotion ? undefined : "empty-illustration__dash"}
        d="M104 116 Q160 72 216 116"
        stroke={OLIVE}
        strokeWidth="1"
        opacity="0.5"
      />
      <circle cx="160" cy="92" r="12" stroke={STROKE} strokeWidth="1" opacity="0.45" />
      <path d="M154 92 H166 M160 86 V98" stroke={SAND} strokeWidth="1" opacity="0.4" />
      {!reducedMotion && (
        <circle r="2" fill={OLIVE} opacity="0.55">
          <animateMotion dur="18s" repeatCount="indefinite">
            <mpath href={`#${pathId}`} />
          </animateMotion>
        </circle>
      )}
    </svg>
  );
}

function NoResultsArt({ reducedMotion }) {
  return (
    <svg className="empty-state-illustration" viewBox="0 0 280 160" fill="none" aria-hidden="true">
      <g className={reducedMotion ? undefined : "empty-illustration__float-a"} opacity="0.5">
        <rect x="32" y="96" width="72" height="48" rx="8" stroke={STROKE} strokeWidth="1" opacity="0.45" />
        <rect x="108" y="96" width="72" height="48" rx="8" stroke={STROKE} strokeWidth="1" opacity="0.4" />
        <rect x="184" y="96" width="72" height="48" rx="8" stroke={STROKE} strokeWidth="1" opacity="0.35" />
      </g>
      <g className={reducedMotion ? undefined : "empty-illustration__breathe"}>
        <circle cx="140" cy="68" r="22" stroke={STROKE} strokeWidth="1.2" opacity="0.5" />
        <path d="M156 84 L172 100" stroke={STROKE} strokeWidth="1.5" strokeLinecap="round" opacity="0.45" />
        <path
          className={reducedMotion ? undefined : "empty-illustration__dash"}
          d="M128 62 Q140 54 152 62"
          stroke={SAND}
          strokeWidth="1"
          opacity="0.4"
        />
      </g>
      <line x1="48" y1="112" x2="88" y2="112" stroke={STROKE} strokeWidth="1" opacity="0.22" />
      <line x1="124" y1="112" x2="164" y2="112" stroke={STROKE} strokeWidth="1" opacity="0.2" />
      <line x1="200" y1="112" x2="240" y2="112" stroke={STROKE} strokeWidth="1" opacity="0.18" />
    </svg>
  );
}

function EmployerJobsArt({ reducedMotion, pathId }) {
  return (
    <svg className="empty-state-illustration" viewBox="0 0 280 160" fill="none" aria-hidden="true">
      <defs>
        <path
          id={pathId}
          d="M72 80 C 100 80, 108 64, 140 64 C 172 64, 180 80, 208 80"
        />
      </defs>
      <g className={reducedMotion ? undefined : "empty-illustration__float-a"}>
        <rect x="24" y="48" width="96" height="64" rx="10" stroke={STROKE} strokeWidth="1.2" opacity="0.55" />
        <line x1="40" y1="68" x2="104" y2="68" stroke={STROKE} strokeWidth="1" opacity="0.35" />
        <line x1="40" y1="82" x2="88" y2="82" stroke={STROKE} strokeWidth="1" opacity="0.28" />
        <line x1="40" y1="96" x2="72" y2="96" stroke={STROKE} strokeWidth="1" opacity="0.22" />
        <circle cx="36" cy="58" r="4" fill={OLIVE} opacity="0.45" />
      </g>
      <path
        d="M120 80 H160"
        stroke={SAND}
        strokeWidth="1"
        strokeDasharray="4 4"
        opacity="0.45"
      />
      <g className={reducedMotion ? undefined : "empty-illustration__float-b"}>
        <rect x="168" y="36" width="56" height="40" rx="8" stroke={STROKE} strokeWidth="1" opacity="0.45" />
        <circle cx="184" cy="52" r="8" stroke={STROKE} strokeWidth="1" opacity="0.4" />
        <line x1="198" y1="50" x2="214" y2="50" stroke={STROKE} strokeWidth="1" opacity="0.3" />
        <line x1="198" y1="58" x2="208" y2="58" stroke={STROKE} strokeWidth="1" opacity="0.25" />
      </g>
      <g className={reducedMotion ? undefined : "empty-illustration__float-a"} opacity="0.85">
        <rect x="168" y="88" width="56" height="40" rx="8" stroke={STROKE} strokeWidth="1" opacity="0.4" />
        <circle cx="184" cy="104" r="8" stroke={STROKE} strokeWidth="1" opacity="0.38" />
        <line x1="198" y1="102" x2="214" y2="102" stroke={STROKE} strokeWidth="1" opacity="0.28" />
      </g>
      <g className={reducedMotion ? undefined : "empty-illustration__float-b"} opacity="0.7">
        <rect x="232" y="62" width="48" height="36" rx="8" stroke={STROKE} strokeWidth="1" opacity="0.35" />
        <circle cx="246" cy="76" r="7" stroke={STROKE} strokeWidth="1" opacity="0.32" />
      </g>
      {!reducedMotion && (
        <circle r="2" fill={OLIVE} opacity="0.5">
          <animateMotion dur="14s" repeatCount="indefinite">
            <mpath href={`#${pathId}`} />
          </animateMotion>
        </circle>
      )}
    </svg>
  );
}

function JobsSearchArt({ reducedMotion, pathId }) {
  return (
    <svg className="empty-state-illustration empty-state-illustration--jobs" viewBox="0 0 360 200" fill="none" aria-hidden="true">
      <g className="empty-state-ghost-cards" opacity="0.42">
        <g className={reducedMotion ? undefined : "empty-illustration__float-a"}>
          <rect x="20" y="108" width="88" height="56" rx="10" stroke={STROKE} strokeWidth="1" />
          <line x1="36" y1="128" x2="92" y2="128" stroke={STROKE} strokeWidth="1" opacity="0.35" />
          <line x1="36" y1="142" x2="76" y2="142" stroke={STROKE} strokeWidth="1" opacity="0.28" />
        </g>
        <g className={reducedMotion ? undefined : "empty-illustration__float-b"}>
          <rect x="136" y="118" width="88" height="56" rx="10" stroke={STROKE} strokeWidth="1" opacity="0.85" />
          <rect x="152" y="132" width="16" height="16" rx="4" stroke={STROKE} strokeWidth="1" opacity="0.35" />
          <line x1="174" y1="136" x2="208" y2="136" stroke={STROKE} strokeWidth="1" opacity="0.32" />
          <line x1="174" y1="150" x2="198" y2="150" stroke={STROKE} strokeWidth="1" opacity="0.26" />
        </g>
        <g className={reducedMotion ? undefined : "empty-illustration__float-a"} opacity="0.72">
          <rect x="252" y="104" width="88" height="56" rx="10" stroke={STROKE} strokeWidth="1" />
          <line x1="268" y1="124" x2="324" y2="124" stroke={STROKE} strokeWidth="1" opacity="0.32" />
          <line x1="268" y1="138" x2="304" y2="138" stroke={STROKE} strokeWidth="1" opacity="0.26" />
        </g>
      </g>
      <path
        id={pathId}
        className={reducedMotion ? undefined : "empty-illustration__dash"}
        d="M108 136 Q180 72 252 136"
        stroke={OLIVE}
        strokeWidth="1.2"
        opacity="0.55"
      />
      <circle cx="180" cy="88" r="14" stroke={STROKE} strokeWidth="1.2" opacity="0.5" />
      <path d="M174 88 H186 M180 82 V94" stroke={SAND} strokeWidth="1" opacity="0.45" />
      {!reducedMotion && (
        <circle r="2.5" fill={OLIVE} opacity="0.6">
          <animateMotion dur="16s" repeatCount="indefinite">
            <mpath href={`#${pathId}`} />
          </animateMotion>
        </circle>
      )}
    </svg>
  );
}

/**
 * @param {"profile-needed"|"ready"|"jobs-search"|"no-results"|"employer-jobs"} variant
 */
export default function EmptyStateIllustration({ variant = "ready" }) {
  const rawId = useId().replace(/:/g, "");
  const readyPathId = `empty-ready-path-${rawId}`;
  const jobsSearchPathId = `empty-jobs-search-path-${rawId}`;
  const employerPathId = `empty-employer-path-${rawId}`;
  const reducedMotion = useReducedMotion();

  switch (variant) {
    case "profile-needed":
      return <ProfileNeededArt reducedMotion={reducedMotion} />;
    case "jobs-search":
      return <JobsSearchArt reducedMotion={reducedMotion} pathId={jobsSearchPathId} />;
    case "no-results":
      return <NoResultsArt reducedMotion={reducedMotion} />;
    case "employer-jobs":
      return <EmployerJobsArt reducedMotion={reducedMotion} pathId={employerPathId} />;
    case "ready":
    default:
      return <ReadyArt reducedMotion={reducedMotion} pathId={readyPathId} />;
  }
}
