export default function ProfileStrength({ percent, hint }) {
  const filled = Math.round(percent / 10);
  return (
    <div className="profile-strength">
      <div className="profile-strength-head">
        <span>Profile strength: {percent}%</span>
      </div>
      <div className="profile-strength-bar" aria-hidden="true">
        {Array.from({ length: 10 }).map((_, i) => (
          <span key={i} className={i < filled ? "filled" : ""} />
        ))}
      </div>
      <p className="profile-strength-hint">{hint}</p>
    </div>
  );
}
