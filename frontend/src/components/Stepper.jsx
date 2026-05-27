import { IconCheck } from "./icons.jsx";

export default function Stepper({ steps, current }) {
  return (
    <nav className="stepper" aria-label="Progress">
      {steps.map((step, i) => {
        const num = i + 1;
        const done = num < current;
        const active = num === current;
        return (
          <div key={step} className={`stepper-item${done ? " done" : ""}${active ? " active" : ""}`}>
            <span className="stepper-marker" aria-hidden="true">
              {done ? <IconCheck size={12} /> : num}
            </span>
            <span className="stepper-label">{step}</span>
            {i < steps.length - 1 && <span className="stepper-connector" aria-hidden="true" />}
          </div>
        );
      })}
    </nav>
  );
}
