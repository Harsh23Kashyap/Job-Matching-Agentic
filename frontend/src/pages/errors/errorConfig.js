export const ERROR_CODES = [401, 402, 403, 501, 502];

export const ERROR_CONTENT = {
  401: {
    title: "Sign in required",
    description:
      "You need to be signed in to view this page. Sign in with your JobMatch account or create one to continue.",
    primary: { label: "Sign in", to: "/login" },
    secondary: { label: "Create account", to: "/register" },
    tone: "auth",
  },
  402: {
    title: "Upgrade to continue",
    description:
      "This feature is part of JobMatch Premium — advanced matching, priority listings, and team analytics. Upgrade your plan to unlock it.",
    primary: { label: "View plans", to: "/register" },
    secondary: { label: "Back to home", to: "/" },
    tone: "premium",
  },
  403: {
    title: "Access denied",
    description:
      "Your account doesn't have permission to open this page. You may be signed in with the wrong role — try your own portal instead.",
    primary: { label: "Go to my portal", action: "roleHome" },
    secondary: { label: "Sign in as someone else", to: "/login" },
    tone: "forbidden",
  },
  501: {
    title: "Not implemented yet",
    description:
      "This capability isn't available in the current release. We're still building it — check back after the next update or use the admin console for eval features.",
    primary: { label: "Go to home", to: "/" },
    secondary: { label: "Admin console", to: "/admin/console" },
    tone: "wip",
  },
  502: {
    title: "Service unavailable",
    description:
      "JobMatch couldn't reach the API server. Make sure the backend is running on port 8001, then try again.",
    primary: { label: "Try again", action: "reload" },
    secondary: { label: "Back to home", to: "/" },
    tone: "outage",
  },
};
