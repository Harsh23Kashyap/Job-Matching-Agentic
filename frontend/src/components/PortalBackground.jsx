import { useLocation } from "react-router-dom";
import BackgroundOrnaments from "./BackgroundOrnaments.jsx";
import { resolveBackgroundVariant } from "../utils/portalBackground.js";

export default function PortalBackground() {
  const { pathname } = useLocation();
  const variant = resolveBackgroundVariant(pathname);

  return <BackgroundOrnaments variant={variant} scope="page" />;
}
