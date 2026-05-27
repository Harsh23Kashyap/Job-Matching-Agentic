import { useId } from "react";
import { useReducedMotion } from "../hooks/useReducedMotion.js";

const STROKE = "#52635A";
const SAND = "#7A6348";
const OLIVE = "#6E8B74";

function DotGrid({ patternId }) {
  return (
    <svg className="bg-pattern__grid" aria-hidden="true" preserveAspectRatio="none">
      <defs>
        <pattern id={patternId} width="28" height="28" patternUnits="userSpaceOnUse">
          <circle cx="1" cy="1" r="0.9" fill="currentColor" opacity="0.45" />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill={`url(#${patternId})`} />
    </svg>
  );
}

function OnboardingArt({ reducedMotion }) {
  return (
    <>
      <svg className="bg-pattern__layer bg-pattern__doc bg-pattern__float-a" viewBox="0 0 120 160" fill="none" aria-hidden="true">
        <rect x="8" y="8" width="104" height="144" rx="10" stroke={STROKE} strokeWidth="1" />
        <line x1="28" y1="36" x2="92" y2="36" stroke={STROKE} strokeWidth="1" opacity="0.55" />
        <line x1="28" y1="56" x2="80" y2="56" stroke={STROKE} strokeWidth="1" opacity="0.4" />
        <line x1="28" y1="72" x2="70" y2="72" stroke={STROKE} strokeWidth="1" opacity="0.3" />
      </svg>
      <svg className="bg-pattern__layer bg-pattern__arrow bg-pattern__float-b" viewBox="0 0 80 80" fill="none" aria-hidden="true">
        <path d="M40 58 V26 M40 26 L30 36 M40 26 L50 36" stroke={STROKE} strokeWidth="1" strokeLinecap="round" />
        <path
          className={reducedMotion ? undefined : "bg-pattern__dash"}
          d="M40 58 Q40 44 52 38"
          stroke={STROKE}
          strokeWidth="1"
        />
      </svg>
      <svg className="bg-pattern__layer bg-pattern__mini-card bg-pattern__breathe" viewBox="0 0 88 56" fill="none" aria-hidden="true">
        <rect x="4" y="4" width="80" height="48" rx="8" stroke={STROKE} strokeWidth="1" />
        <circle cx="24" cy="28" r="8" stroke={STROKE} strokeWidth="1" opacity="0.45" />
        <line x1="38" y1="24" x2="68" y2="24" stroke={STROKE} strokeWidth="1" opacity="0.35" />
        <line x1="38" y1="34" x2="58" y2="34" stroke={STROKE} strokeWidth="1" opacity="0.28" />
      </svg>
    </>
  );
}

function ProfileArt() {
  return (
    <>
      <svg className="bg-pattern__layer bg-pattern__profile-card bg-pattern__float-a" viewBox="0 0 140 100" fill="none" aria-hidden="true">
        <rect x="8" y="8" width="124" height="84" rx="10" stroke={STROKE} strokeWidth="1" />
        <circle cx="40" cy="40" r="14" stroke={STROKE} strokeWidth="1" opacity="0.45" />
        <line x1="64" y1="34" x2="112" y2="34" stroke={STROKE} strokeWidth="1.5" opacity="0.35" />
        <line x1="64" y1="50" x2="96" y2="50" stroke={STROKE} strokeWidth="1" opacity="0.28" />
      </svg>
      <svg className="bg-pattern__layer bg-pattern__checklist bg-pattern__float-b" viewBox="0 0 100 120" fill="none" aria-hidden="true">
        <circle cx="14" cy="24" r="3" stroke={STROKE} strokeWidth="1" opacity="0.5" />
        <circle cx="14" cy="48" r="3" stroke={STROKE} strokeWidth="1" opacity="0.45" />
        <circle cx="14" cy="72" r="3" stroke={STROKE} strokeWidth="1" opacity="0.4" />
        <line x1="24" y1="24" x2="80" y2="24" stroke={STROKE} strokeWidth="1" opacity="0.35" />
        <line x1="24" y1="48" x2="72" y2="48" stroke={STROKE} strokeWidth="1" opacity="0.3" />
        <line x1="24" y1="72" x2="64" y2="72" stroke={STROKE} strokeWidth="1" opacity="0.25" />
        <path d="M8 24 L12 28 L18 20" stroke={STROKE} strokeWidth="1" opacity="0.4" />
        <path d="M8 48 L12 52 L18 44" stroke={STROKE} strokeWidth="1" opacity="0.35" />
      </svg>
    </>
  );
}

function JobsArt({ reducedMotion, pathAId, pathBId }) {
  return (
    <>
      <svg className="bg-pattern__layer bg-pattern__jobs-scene" viewBox="0 0 900 500" fill="none" aria-hidden="true">
        <path
          id={pathAId}
          d="M100 350 Q280 250 450 300 T780 280"
          stroke={STROKE}
          strokeWidth="1"
          fill="none"
          opacity="0.55"
        />
        <path
          id={pathBId}
          className={reducedMotion ? undefined : "bg-pattern__dash"}
          d="M140 120 Q320 80 500 140 T820 100"
          stroke={STROKE}
          strokeWidth="1"
          fill="none"
          opacity="0.45"
        />
        <circle cx="120" cy="350" r="3.5" fill={STROKE} opacity="0.5" />
        <circle cx="450" cy="300" r="3" fill={STROKE} opacity="0.45" />
        <circle cx="780" cy="280" r="3.5" fill={STROKE} opacity="0.5" />
        <circle cx="500" cy="140" r="2.5" fill="#6E8B74" opacity="0.45" />
        {!reducedMotion && (
          <>
            <circle r="2.5" fill="#6E8B74" opacity="0.55">
              <animateMotion dur="22s" repeatCount="indefinite">
                <mpath href={`#${pathAId}`} />
              </animateMotion>
            </circle>
            <circle r="2" fill="#7A6348" opacity="0.5">
              <animateMotion dur="28s" repeatCount="indefinite">
                <mpath href={`#${pathBId}`} />
              </animateMotion>
            </circle>
          </>
        )}
      </svg>
      <svg className="bg-pattern__layer bg-pattern__job-card bg-pattern__job-card--a bg-pattern__float-a" viewBox="0 0 100 72" fill="none" aria-hidden="true">
        <rect x="4" y="4" width="92" height="64" rx="8" stroke={STROKE} strokeWidth="1" />
        <rect x="20" y="18" width="24" height="24" rx="4" stroke={STROKE} strokeWidth="1" opacity="0.35" />
        <line x1="52" y1="22" x2="76" y2="22" stroke={STROKE} strokeWidth="1" opacity="0.35" />
      </svg>
      <svg className="bg-pattern__layer bg-pattern__job-card bg-pattern__job-card--b bg-pattern__float-b" viewBox="0 0 100 72" fill="none" aria-hidden="true">
        <rect x="4" y="4" width="92" height="64" rx="8" stroke={STROKE} strokeWidth="1" />
        <line x1="20" y1="20" x2="72" y2="20" stroke={STROKE} strokeWidth="1" opacity="0.35" />
        <line x1="20" y1="34" x2="56" y2="34" stroke={STROKE} strokeWidth="1" opacity="0.28" />
      </svg>
    </>
  );
}

function EmptyArt({ reducedMotion, pathId }) {
  return (
    <svg className="bg-pattern__layer bg-pattern__empty-scene" viewBox="0 0 360 200" fill="none" aria-hidden="true">
      <rect x="24" y="88" width="88" height="64" rx="10" stroke={STROKE} strokeWidth="1" opacity="0.55" />
      <circle cx="48" cy="112" r="9" stroke={STROKE} strokeWidth="1" opacity="0.4" />
      <line x1="66" y1="106" x2="98" y2="106" stroke={STROKE} strokeWidth="1" opacity="0.32" />
      <line x1="66" y1="120" x2="88" y2="120" stroke={STROKE} strokeWidth="1" opacity="0.26" />

      <rect x="248" y="88" width="88" height="64" rx="10" stroke={STROKE} strokeWidth="1" opacity="0.55" />
      <rect x="264" y="104" width="18" height="18" rx="4" stroke={STROKE} strokeWidth="1" opacity="0.35" />
      <line x1="290" y1="108" x2="318" y2="108" stroke={STROKE} strokeWidth="1" opacity="0.32" />

      <path
        id={pathId}
        className={reducedMotion ? undefined : "bg-pattern__dash"}
        d="M112 120 Q180 72 248 120"
        stroke={STROKE}
        strokeWidth="1"
        opacity="0.5"
      />
      <circle cx="180" cy="96" r="14" stroke={STROKE} strokeWidth="1" opacity="0.45" />
      <path d="M174 96 H186 M180 90 V102" stroke={STROKE} strokeWidth="1" opacity="0.4" />
      {!reducedMotion && (
        <circle r="2" fill={OLIVE} opacity="0.55">
          <animateMotion dur="20s" repeatCount="indefinite">
            <mpath href={`#${pathId}`} />
          </animateMotion>
        </circle>
      )}
    </svg>
  );
}

function EmployerJobsArt({ reducedMotion, pathAId, pathBId, pathCId }) {
  return (
    <>
      <svg className="bg-pattern__layer bg-pattern__employer-jobs-scene" viewBox="0 0 900 520" fill="none" aria-hidden="true">
        <rect x="72" y="196" width="128" height="88" rx="10" stroke={STROKE} strokeWidth="1" opacity="0.5" />
        <line x1="96" y1="224" x2="176" y2="224" stroke={STROKE} strokeWidth="1" opacity="0.35" />
        <line x1="96" y1="244" x2="152" y2="244" stroke={STROKE} strokeWidth="1" opacity="0.28" />
        <line x1="96" y1="260" x2="136" y2="260" stroke={STROKE} strokeWidth="1" opacity="0.22" />

        <g opacity="0.48">
          <rect x="108" y="148" width="56" height="40" rx="4" stroke={SAND} strokeWidth="1" />
          <rect x="118" y="158" width="10" height="10" rx="1" stroke={SAND} strokeWidth="0.8" opacity="0.55" />
          <rect x="134" y="158" width="10" height="10" rx="1" stroke={SAND} strokeWidth="0.8" opacity="0.55" />
          <rect x="150" y="158" width="10" height="10" rx="1" stroke={SAND} strokeWidth="0.8" opacity="0.55" />
          <rect x="126" y="174" width="20" height="14" rx="1" stroke={SAND} strokeWidth="0.8" opacity="0.45" />
        </g>

        <circle cx="480" cy="208" r="22" stroke={STROKE} strokeWidth="1" opacity="0.42" />
        <circle cx="480" cy="208" r="9" stroke={STROKE} strokeWidth="1" opacity="0.35" />
        <line x1="498" y1="202" x2="528" y2="202" stroke={STROKE} strokeWidth="1" opacity="0.28" />
        <line x1="498" y1="214" x2="516" y2="214" stroke={STROKE} strokeWidth="1" opacity="0.22" />

        <circle cx="620" cy="168" r="18" stroke={OLIVE} strokeWidth="1" opacity="0.4" />
        <circle cx="620" cy="168" r="7" stroke={OLIVE} strokeWidth="1" opacity="0.32" />

        <circle cx="680" cy="268" r="20" stroke={STROKE} strokeWidth="1" opacity="0.38" />
        <circle cx="680" cy="268" r="8" stroke={STROKE} strokeWidth="1" opacity="0.3" />

        <path
          id={pathAId}
          d="M200 240 Q340 220 458 210"
          stroke={STROKE}
          strokeWidth="1"
          fill="none"
          opacity="0.45"
        />
        <path
          id={pathBId}
          className={reducedMotion ? undefined : "bg-pattern__dash"}
          d="M200 232 Q380 160 602 168"
          stroke={SAND}
          strokeWidth="1"
          fill="none"
          opacity="0.4"
        />
        <path
          id={pathCId}
          className={reducedMotion ? undefined : "bg-pattern__dash"}
          d="M200 248 Q420 300 660 268"
          stroke={OLIVE}
          strokeWidth="1"
          fill="none"
          opacity="0.38"
        />
        {!reducedMotion && (
          <>
            <circle r="2.5" fill={OLIVE} opacity="0.5">
              <animateMotion dur="28s" repeatCount="indefinite">
                <mpath href={`#${pathAId}`} />
              </animateMotion>
            </circle>
            <circle r="2" fill={SAND} opacity="0.45">
              <animateMotion dur="32s" repeatCount="indefinite">
                <mpath href={`#${pathBId}`} />
              </animateMotion>
            </circle>
            <circle r="2" fill={STROKE} opacity="0.42">
              <animateMotion dur="26s" repeatCount="indefinite">
                <mpath href={`#${pathCId}`} />
              </animateMotion>
            </circle>
          </>
        )}
      </svg>
      <svg className="bg-pattern__layer bg-pattern__employer-job-card bg-pattern__employer-job-card--a bg-pattern__float-a" viewBox="0 0 100 72" fill="none" aria-hidden="true">
        <rect x="4" y="4" width="92" height="64" rx="8" stroke={STROKE} strokeWidth="1" opacity="0.48" />
        <line x1="20" y1="22" x2="72" y2="22" stroke={STROKE} strokeWidth="1" opacity="0.32" />
        <line x1="20" y1="36" x2="56" y2="36" stroke={STROKE} strokeWidth="1" opacity="0.26" />
      </svg>
      <svg className="bg-pattern__layer bg-pattern__employer-job-card bg-pattern__employer-job-card--b bg-pattern__float-b" viewBox="0 0 100 72" fill="none" aria-hidden="true">
        <rect x="4" y="4" width="92" height="64" rx="8" stroke={STROKE} strokeWidth="1" opacity="0.42" />
        <rect x="18" y="18" width="22" height="22" rx="4" stroke={SAND} strokeWidth="1" opacity="0.35" />
        <line x1="48" y1="24" x2="74" y2="24" stroke={STROKE} strokeWidth="1" opacity="0.28" />
      </svg>
    </>
  );
}

function EmployerCandidatesArt({ reducedMotion, pathAId, pathBId, pathCId }) {
  return (
    <>
      <svg className="bg-pattern__layer bg-pattern__employer-candidates-scene" viewBox="0 0 900 520" fill="none" aria-hidden="true">
        <circle cx="450" cy="260" r="6" fill={STROKE} opacity="0.45" />
        <circle cx="380" cy="220" r="4" fill={OLIVE} opacity="0.4" />
        <circle cx="520" cy="220" r="4" fill={SAND} opacity="0.38" />
        <circle cx="400" cy="310" r="4" fill={STROKE} opacity="0.35" />
        <circle cx="500" cy="300" r="4" fill={OLIVE} opacity="0.35" />
        <line x1="450" y1="260" x2="380" y2="220" stroke={STROKE} strokeWidth="1" opacity="0.28" />
        <line x1="450" y1="260" x2="520" y2="220" stroke={STROKE} strokeWidth="1" opacity="0.28" />
        <line x1="450" y1="260" x2="400" y2="310" stroke={STROKE} strokeWidth="1" opacity="0.24" />
        <line x1="450" y1="260" x2="500" y2="300" stroke={STROKE} strokeWidth="1" opacity="0.24" />

        <path id={pathAId} d="M120 140 Q280 180 380 220" stroke={STROKE} strokeWidth="1" fill="none" opacity="0.42" />
        <path
          id={pathBId}
          className={reducedMotion ? undefined : "bg-pattern__dash"}
          d="M780 140 Q620 180 520 220"
          stroke={SAND}
          strokeWidth="1"
          fill="none"
          opacity="0.38"
        />
        <path
          id={pathCId}
          className={reducedMotion ? undefined : "bg-pattern__dash"}
          d="M160 380 Q320 340 400 310"
          stroke={OLIVE}
          strokeWidth="1"
          fill="none"
          opacity="0.36"
        />

        {!reducedMotion && (
          <>
            <circle r="2.5" fill={OLIVE} opacity="0.48">
              <animateMotion dur="30s" repeatCount="indefinite">
                <mpath href={`#${pathAId}`} />
              </animateMotion>
            </circle>
            <circle r="2" fill={SAND} opacity="0.42">
              <animateMotion dur="34s" repeatCount="indefinite">
                <mpath href={`#${pathBId}`} />
              </animateMotion>
            </circle>
            <circle r="2" fill={STROKE} opacity="0.4">
              <animateMotion dur="27s" repeatCount="indefinite">
                <mpath href={`#${pathCId}`} />
              </animateMotion>
            </circle>
          </>
        )}
      </svg>
      <svg className="bg-pattern__layer bg-pattern__employer-profile-card bg-pattern__employer-profile-card--a bg-pattern__float-a" viewBox="0 0 108 76" fill="none" aria-hidden="true">
        <rect x="4" y="4" width="100" height="68" rx="8" stroke={STROKE} strokeWidth="1" opacity="0.48" />
        <circle cx="30" cy="32" r="11" stroke={STROKE} strokeWidth="1" opacity="0.38" />
        <line x1="50" y1="28" x2="88" y2="28" stroke={STROKE} strokeWidth="1" opacity="0.3" />
        <line x1="50" y1="42" x2="76" y2="42" stroke={STROKE} strokeWidth="1" opacity="0.24" />
      </svg>
      <svg className="bg-pattern__layer bg-pattern__employer-profile-card bg-pattern__employer-profile-card--b bg-pattern__float-b" viewBox="0 0 108 76" fill="none" aria-hidden="true">
        <rect x="4" y="4" width="100" height="68" rx="8" stroke={STROKE} strokeWidth="1" opacity="0.42" />
        <circle cx="30" cy="32" r="11" stroke={OLIVE} strokeWidth="1" opacity="0.35" />
        <line x1="50" y1="28" x2="84" y2="28" stroke={STROKE} strokeWidth="1" opacity="0.28" />
        <line x1="50" y1="42" x2="70" y2="42" stroke={STROKE} strokeWidth="1" opacity="0.22" />
      </svg>
      <svg className="bg-pattern__layer bg-pattern__employer-profile-card bg-pattern__employer-profile-card--c bg-pattern__breathe" viewBox="0 0 108 76" fill="none" aria-hidden="true">
        <rect x="4" y="4" width="100" height="68" rx="8" stroke={STROKE} strokeWidth="1" opacity="0.38" />
        <circle cx="30" cy="32" r="11" stroke={SAND} strokeWidth="1" opacity="0.32" />
        <line x1="50" y1="28" x2="80" y2="28" stroke={STROKE} strokeWidth="1" opacity="0.26" />
      </svg>
    </>
  );
}

function EmployerEmptyArt({ reducedMotion, pathAId, pathBId, pathCId }) {
  return (
    <svg className="bg-pattern__layer bg-pattern__employer-empty-scene" viewBox="0 0 420 240" fill="none" aria-hidden="true">
      <rect x="24" y="72" width="136" height="96" rx="12" stroke={STROKE} strokeWidth="1.2" opacity="0.55" />
      <line x1="44" y1="98" x2="140" y2="98" stroke={STROKE} strokeWidth="1" opacity="0.35" />
      <line x1="44" y1="118" x2="116" y2="118" stroke={STROKE} strokeWidth="1" opacity="0.28" />
      <line x1="44" y1="136" x2="96" y2="136" stroke={STROKE} strokeWidth="1" opacity="0.22" />
      <rect x="52" y="52" width="48" height="32" rx="4" stroke={SAND} strokeWidth="1" opacity="0.4" />

      <rect x="248" y="48" width="72" height="52" rx="8" stroke={STROKE} strokeWidth="1" opacity="0.45" />
      <circle cx="268" cy="68" r="8" stroke={STROKE} strokeWidth="1" opacity="0.35" />
      <line x1="284" y1="64" x2="304" y2="64" stroke={STROKE} strokeWidth="1" opacity="0.28" />
      <line x1="284" y1="76" x2="298" y2="76" stroke={STROKE} strokeWidth="1" opacity="0.22" />

      <rect x="248" y="118" width="72" height="52" rx="8" stroke={STROKE} strokeWidth="1" opacity="0.42" />
      <circle cx="268" cy="138" r="8" stroke={OLIVE} strokeWidth="1" opacity="0.32" />
      <line x1="284" y1="134" x2="304" y2="134" stroke={STROKE} strokeWidth="1" opacity="0.26" />

      <rect x="248" y="168" width="72" height="52" rx="8" stroke={STROKE} strokeWidth="1" opacity="0.38" />
      <circle cx="268" cy="188" r="8" stroke={SAND} strokeWidth="1" opacity="0.3" />
      <line x1="284" y1="184" x2="300" y2="184" stroke={STROKE} strokeWidth="1" opacity="0.24" />

      <path id={pathAId} d="M160 120 Q204 74 248 74" stroke={STROKE} strokeWidth="1" fill="none" opacity="0.45" />
      <path
        id={pathBId}
        className={reducedMotion ? undefined : "bg-pattern__dash"}
        d="M160 120 Q204 120 248 144"
        stroke={SAND}
        strokeWidth="1"
        fill="none"
        opacity="0.4"
      />
      <path
        id={pathCId}
        className={reducedMotion ? undefined : "bg-pattern__dash"}
        d="M160 124 Q204 168 248 194"
        stroke={OLIVE}
        strokeWidth="1"
        fill="none"
        opacity="0.36"
      />
      {!reducedMotion && (
        <>
          <circle r="2" fill={OLIVE} opacity="0.45">
            <animateMotion dur="24s" repeatCount="indefinite">
              <mpath href={`#${pathAId}`} />
            </animateMotion>
          </circle>
          <circle r="2" fill={SAND} opacity="0.4">
            <animateMotion dur="28s" repeatCount="indefinite">
              <mpath href={`#${pathBId}`} />
            </animateMotion>
          </circle>
          <circle r="2" fill={STROKE} opacity="0.38">
            <animateMotion dur="22s" repeatCount="indefinite">
              <mpath href={`#${pathCId}`} />
            </animateMotion>
          </circle>
        </>
      )}
    </svg>
  );
}

function VariantArt({
  variant,
  reducedMotion,
  pathAId,
  pathBId,
  emptyPathId,
  employerPathAId,
  employerPathBId,
  employerPathCId,
}) {
  switch (variant) {
    case "onboarding":
      return <OnboardingArt reducedMotion={reducedMotion} />;
    case "profile":
      return <ProfileArt />;
    case "jobs":
      return <JobsArt reducedMotion={reducedMotion} pathAId={pathAId} pathBId={pathBId} />;
    case "empty":
      return <EmptyArt reducedMotion={reducedMotion} pathId={emptyPathId} />;
    case "employer-jobs":
      return (
        <EmployerJobsArt
          reducedMotion={reducedMotion}
          pathAId={employerPathAId}
          pathBId={employerPathBId}
          pathCId={employerPathCId}
        />
      );
    case "employer-candidates":
      return (
        <EmployerCandidatesArt
          reducedMotion={reducedMotion}
          pathAId={employerPathAId}
          pathBId={employerPathBId}
          pathCId={employerPathCId}
        />
      );
    case "employer-empty":
      return (
        <EmployerEmptyArt
          reducedMotion={reducedMotion}
          pathAId={employerPathAId}
          pathBId={employerPathBId}
          pathCId={employerPathCId}
        />
      );
    default:
      return null;
  }
}

/**
 * Subtle animated SVG backgrounds for portal pages.
 * @param {"onboarding"|"profile"|"jobs"|"empty"|"employer-jobs"|"employer-candidates"|"employer-empty"|"base"} variant
 * @param {"page"|"panel"|"inline"} scope
 */
export default function BackgroundPattern({ variant = "base", scope = "page" }) {
  const rawId = useId().replace(/:/g, "");
  const patternId = `bg-dots-${rawId}`;
  const pathAId = `bg-path-a-${rawId}`;
  const pathBId = `bg-path-b-${rawId}`;
  const emptyPathId = `bg-empty-path-${rawId}`;
  const employerPathAId = `bg-employer-path-a-${rawId}`;
  const employerPathBId = `bg-employer-path-b-${rawId}`;
  const employerPathCId = `bg-employer-path-c-${rawId}`;
  const reducedMotion = useReducedMotion();

  return (
    <div
      className={`bg-pattern bg-pattern--${scope}${variant !== "base" ? ` bg-pattern--${variant}` : ""}${reducedMotion ? " bg-pattern--static" : ""}`}
      aria-hidden="true"
    >
      <DotGrid patternId={patternId} />
      <VariantArt
        variant={variant}
        reducedMotion={reducedMotion}
        pathAId={pathAId}
        pathBId={pathBId}
        emptyPathId={emptyPathId}
        employerPathAId={employerPathAId}
        employerPathBId={employerPathBId}
        employerPathCId={employerPathCId}
      />
    </div>
  );
}
