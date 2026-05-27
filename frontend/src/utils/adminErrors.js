/** Map raw API / backend errors to admin-friendly copy. */
export function parseAdminError(raw) {
  if (!raw) {
    return {
      title: "Something went wrong",
      summary: "An unexpected error occurred. Try again or check the backend logs.",
      details: null,
      severity: "error",
    };
  }

  const text = String(raw);

  if (/already accessed by another instance|Storage folder.*Qdrant|qdrant_db/i.test(text)) {
    return {
      title: "Vector store is locked",
      summary:
        "Another Qdrant process is using this storage folder. Stop the other process or switch to Qdrant server mode.",
      details: text,
      severity: "error",
    };
  }

  if (/404|not found/i.test(text) && /agents|status/i.test(text)) {
    return {
      title: "Backend offline",
      summary: "Start the API on port 8001 (see README).",
      details: text,
      severity: "error",
    };
  }

  if (/network|fetch|ECONNREFUSED/i.test(text)) {
    return {
      title: "Cannot reach backend",
      summary: "Check that the API server is running and your network connection is stable.",
      details: text,
      severity: "error",
    };
  }

  const short = text.length <= 140;
  return {
    title: "Request failed",
    summary: short ? text : `${text.slice(0, 140)}…`,
    details: short ? null : text,
    severity: "error",
  };
}
