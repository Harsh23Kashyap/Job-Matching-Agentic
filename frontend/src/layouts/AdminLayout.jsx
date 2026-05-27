import { IconConsole } from "../components/icons.jsx";
import PortalShell from "./PortalShell.jsx";

const NAV = [{ to: "/admin/console", label: "Console", icon: <IconConsole size={20} /> }];

export default function AdminLayout() {
  return <PortalShell subtitle="Admin" navItems={NAV} />;
}
