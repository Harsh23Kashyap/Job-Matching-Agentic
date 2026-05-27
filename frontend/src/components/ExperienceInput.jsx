export default function ExperienceInput({ id, value, onChange, error }) {
  return (
    <div className={`experience-input-wrap${error ? " has-error" : ""}`}>
      <input
        id={id}
        type="text"
        inputMode="decimal"
        className="experience-input input-no-spinner"
        placeholder="2"
        value={value ?? ""}
        onChange={(e) => onChange(e.target.value)}
      />
      <span className="experience-suffix">years</span>
    </div>
  );
}
