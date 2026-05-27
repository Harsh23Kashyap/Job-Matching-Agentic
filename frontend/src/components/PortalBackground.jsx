import { useLocation } from "react-router-dom";
import BackgroundPattern from "./BackgroundPattern.jsx";

function resolveVariant(pathname) {
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

export default function PortalBackground() {
  const { pathname } = useLocation();
  const variant = resolveVariant(pathname);

  return <BackgroundPattern variant={variant} scope="page" />;
}
