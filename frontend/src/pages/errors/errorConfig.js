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
      "This feature needs a JobMatch Premium plan (advanced matching, priority listings, team analytics).",
    primary: { label: "View plans", to: "/register" },
    secondary: { label: "Back to home", to: "/" },
    tone: "premium",
  },
  403: {
    title: "Access denied",
    description:
      "Your account can't open this page. You may be signed in with the wrong role; use your own portal instead.",
    primary: { label: "Go to my portal", action: "roleHome" },
    secondary: { label: "Sign in as someone else", to: "/login" },
    tone: "forbidden",
  },
  501: {
    title: "Not implemented yet",
    description:
      "Not available in this release yet. Check back after the next update, or use the admin console for eval tools.",
    primary: { label: "Go to home", to: "/" },
    secondary: { label: "Admin console", to: "/admin/console" },
    tone: "wip",
  },
  502: {
    title: "Server is taking a break",
    description: "We couldn't reach JobMatch right now. Please try again in a moment.",
    primary: { label: "Try again", action: "reload" },
    secondary: { label: "Go home", to: "/" },
    tone: "outage",
  },
};
