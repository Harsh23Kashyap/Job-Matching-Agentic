import { IconBriefcase, IconSearch } from "../components/icons.jsx";
import PortalShell from "./PortalShell.jsx";

const NAV = [
  { to: "/employer/jobs", label: "My jobs", icon: <IconBriefcase size={20} />, end: true },
  { to: "/employer/matches", label: "Candidates", icon: <IconSearch size={20} />, end: true },
  { to: "/employer/applications", label: "Applicants", icon: <IconBriefcase size={20} />, end: true },
];

export default function EmployerLayout() {
  return <PortalShell portal="employer" subtitle="For employers" navItems={NAV} />;
}
