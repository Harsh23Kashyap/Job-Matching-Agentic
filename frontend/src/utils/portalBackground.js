/** Map portal routes to BackgroundOrnaments variants. */
export function resolveBackgroundVariant(pathname) {
  if (pathname.includes("/admin")) return "admin";
  if (pathname.includes("/candidate/onboarding")) return "onboarding";
  if (pathname.includes("/candidate/profile")) return "profile";
  if (pathname.includes("/employer/jobs")) return "employer-jobs";
  if (pathname.includes("/employer/matches") || pathname.includes("/employer/applications")) {
    return "employer-candidates";
  }
  if (
    pathname.includes("/candidate/matches")
    || pathname.includes("/candidate/saved")
  ) {
    return "jobs";
  }
  return "base";
}

export const BACKGROUND_VARIANTS = [
  "admin",
  "onboarding",
  "profile",
  "employer-jobs",
  "employer-candidates",
  "jobs",
  "base",
];
