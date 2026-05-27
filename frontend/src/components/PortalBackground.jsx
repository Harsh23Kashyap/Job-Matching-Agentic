import { useLocation } from "react-router-dom";

function BaseLayer() {
  return (
    <>
      <svg className="portal-bg-grid" aria-hidden="true">
        <defs>
          <pattern id="portal-dots" width="28" height="28" patternUnits="userSpaceOnUse">
            <circle cx="1" cy="1" r="1" fill="currentColor" opacity="0.35" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#portal-dots)" />
      </svg>
    </>
  );
}

function ResumeLayer() {
  return (
    <>
      <svg className="portal-bg-resume-doc" viewBox="0 0 120 160" fill="none" aria-hidden="true">
        <rect x="8" y="8" width="104" height="144" rx="10" stroke="#52635A" strokeWidth="1" />
        <line x1="28" y1="36" x2="92" y2="36" stroke="#52635A" strokeWidth="1" opacity="0.5" />
        <line x1="28" y1="56" x2="80" y2="56" stroke="#52635A" strokeWidth="1" opacity="0.35" />
        <line x1="28" y1="72" x2="70" y2="72" stroke="#52635A" strokeWidth="1" opacity="0.25" />
      </svg>
      <svg className="portal-bg-resume-arrow" viewBox="0 0 80 80" fill="none" aria-hidden="true">
        <path d="M40 58 V26 M40 26 L30 36 M40 26 L50 36" stroke="#52635A" strokeWidth="1" strokeLinecap="round" />
        <path d="M40 58 Q40 44 52 38" stroke="#52635A" strokeWidth="1" strokeDasharray="3 4" opacity="0.6" />
      </svg>
    </>
  );
}

function ProfilePageLayer() {
  return (
    <>
      <svg className="portal-bg-profile-card" viewBox="0 0 140 100" fill="none" aria-hidden="true">
        <rect x="8" y="8" width="124" height="84" rx="10" stroke="#52635A" strokeWidth="1" />
        <circle cx="40" cy="40" r="14" stroke="#52635A" strokeWidth="1" opacity="0.4" />
        <line x1="64" y1="34" x2="112" y2="34" stroke="#52635A" strokeWidth="1.5" opacity="0.35" />
        <line x1="64" y1="50" x2="96" y2="50" stroke="#52635A" strokeWidth="1" opacity="0.3" />
      </svg>
      <svg className="portal-bg-profile-checklist" viewBox="0 0 100 120" fill="none" aria-hidden="true">
        <line x1="20" y1="24" x2="80" y2="24" stroke="#52635A" strokeWidth="1" opacity="0.35" />
        <line x1="20" y1="48" x2="72" y2="48" stroke="#52635A" strokeWidth="1" opacity="0.3" />
        <line x1="20" y1="72" x2="64" y2="72" stroke="#52635A" strokeWidth="1" opacity="0.25" />
        <path d="M8 24 L12 28 L18 20" stroke="#52635A" strokeWidth="1" opacity="0.4" />
        <path d="M8 48 L12 52 L18 44" stroke="#52635A" strokeWidth="1" opacity="0.35" />
      </svg>
    </>
  );
}

function JobsLayer() {
  return (
    <>
      <svg className="portal-bg-jobs-scene" viewBox="0 0 900 500" fill="none" aria-hidden="true">
        <path id="jobs-path-a" d="M100 350 Q280 250 450 300 T780 280" stroke="#52635A" strokeWidth="1" fill="none" opacity="0.45" />
        <path id="jobs-path-b" d="M140 120 Q320 80 500 140 T820 100" stroke="#52635A" strokeWidth="1" fill="none" opacity="0.35" strokeDasharray="6 8" />
        <circle cx="120" cy="350" r="4" fill="#52635A" opacity="0.5" />
        <circle cx="450" cy="300" r="3" fill="#52635A" opacity="0.4" />
        <circle cx="780" cy="280" r="4" fill="#52635A" opacity="0.5" />
        <circle r="3" fill="#52635A" opacity="0.6">
          <animateMotion dur="18s" repeatCount="indefinite">
            <mpath href="#jobs-path-a" />
          </animateMotion>
        </circle>
      </svg>
      <div className="portal-bg-float-cards" aria-hidden="true">
        <svg className="portal-float-card portal-float-card--job-a" viewBox="0 0 100 72" fill="none">
          <rect x="4" y="4" width="92" height="64" rx="8" stroke="#52635A" strokeWidth="1" fill="#fffdfa" />
          <rect x="20" y="18" width="24" height="24" rx="4" stroke="#52635A" strokeWidth="1" opacity="0.35" />
          <line x1="52" y1="22" x2="76" y2="22" stroke="#52635A" strokeWidth="1" opacity="0.4" />
        </svg>
        <svg className="portal-float-card portal-float-card--job-b" viewBox="0 0 100 72" fill="none">
          <rect x="4" y="4" width="92" height="64" rx="8" stroke="#52635A" strokeWidth="1" fill="#fffdfa" />
          <line x1="20" y1="20" x2="72" y2="20" stroke="#52635A" strokeWidth="1" opacity="0.4" />
        </svg>
      </div>
    </>
  );
}

export function JobsResultsDecor() {
  return (
    <div className="jobs-results-decor" aria-hidden="true">
      <svg className="jobs-results-nodes" viewBox="0 0 800 400" fill="none">
        <path d="M60 300 Q220 220 400 260 T720 240" stroke="#52635A" strokeWidth="1" opacity="0.12" />
        <path d="M100 120 Q280 80 460 130 T740 100" stroke="#52635A" strokeWidth="1" opacity="0.1" strokeDasharray="5 7" />
        <circle cx="220" cy="220" r="3" fill="#52635A" opacity="0.15" />
        <circle cx="400" cy="260" r="4" fill="#52635A" opacity="0.12" />
        <circle cx="580" cy="230" r="3" fill="#52635A" opacity="0.15" />
        <circle r="2.5" fill="#6E8B74" opacity="0.2">
          <animateMotion dur="20s" repeatCount="indefinite">
            <mpath href="#jobs-results-path" />
          </animateMotion>
        </circle>
        <path id="jobs-results-path" d="M60 300 Q220 220 400 260 T720 240" stroke="none" fill="none" />
      </svg>
      <svg className="jobs-results-card jobs-results-card--a" viewBox="0 0 80 56" fill="none">
        <rect x="2" y="2" width="76" height="52" rx="6" stroke="#52635A" strokeWidth="1" opacity="0.12" />
        <line x1="14" y1="14" x2="58" y2="14" stroke="#52635A" strokeWidth="1" opacity="0.1" />
      </svg>
      <svg className="jobs-results-card jobs-results-card--b" viewBox="0 0 80 56" fill="none">
        <rect x="2" y="2" width="76" height="52" rx="6" stroke="#52635A" strokeWidth="1" opacity="0.1" />
        <rect x="14" y="12" width="16" height="16" rx="3" stroke="#52635A" strokeWidth="1" opacity="0.08" />
      </svg>
    </div>
  );
}

export function ResultsDecor() {
  return null;
}

export default function PortalBackground() {
  const { pathname } = useLocation();
  const isOnboarding = pathname.includes("/candidate/onboarding");
  const isProfile = pathname.includes("/candidate/profile");
  const isJobs =
    pathname.includes("/candidate/matches") ||
    pathname.includes("/employer/matches");

  return (
    <div className="portal-background" aria-hidden="true">
      <BaseLayer />
      {isOnboarding && <ResumeLayer />}
      {isProfile && <ProfilePageLayer />}
      {isJobs && <JobsLayer />}
    </div>
  );
}
