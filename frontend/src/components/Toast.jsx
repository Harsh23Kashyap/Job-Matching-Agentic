import { createContext, useCallback, useContext, useMemo, useState } from "react";

const ToastContext = createContext(null);

const VARIANTS = new Set(["success", "error", "info"]);

function parseToastOptions(secondArg) {
  if (secondArg == null) return { variant: "success", action: null };
  if (typeof secondArg === "string" && VARIANTS.has(secondArg)) {
    return { variant: secondArg, action: null };
  }
  if (typeof secondArg === "object" && !secondArg.$$typeof) {
    return {
      variant: VARIANTS.has(secondArg.variant) ? secondArg.variant : "success",
      action: secondArg.action ?? null,
    };
  }
  return { variant: "success", action: secondArg };
}

export function ToastProvider({ children }) {
  const [toast, setToast] = useState(null);

  const showToast = useCallback((message, secondArg) => {
    const { variant, action } = parseToastOptions(secondArg);
    setToast({ message, variant, action });
    setTimeout(() => setToast(null), 5000);
  }, []);

  const value = useMemo(() => ({ showToast }), [showToast]);

  return (
    <ToastContext.Provider value={value}>
      {children}
      {toast && (
        <div className={`toast toast--${toast.variant}`} role="status" aria-live="polite">
          <p>{toast.message}</p>
          {toast.action}
        </div>
      )}
    </ToastContext.Provider>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used within ToastProvider");
  return ctx;
}
