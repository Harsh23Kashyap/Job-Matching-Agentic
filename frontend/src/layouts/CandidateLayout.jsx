import { IconBriefcase, IconProfile, IconUpload } from "../components/icons.jsx";
import PortalShell from "./PortalShell.jsx";

const NAV = [
  { to: "/candidate/onboarding", label: "Resume", icon: <IconUpload size={20} /> },
  { to: "/candidate/profile", label: "Profile", icon: <IconProfile size={20} /> },
  { to: "/candidate/matches", label: "Jobs", icon: <IconBriefcase size={20} /> },
  { to: "/candidate/saved", label: "Saved", icon: <IconBriefcase size={20} /> },
];

export default function CandidateLayout() {
  return <PortalShell portal="candidate" subtitle="For candidates" navItems={NAV} />;
}
