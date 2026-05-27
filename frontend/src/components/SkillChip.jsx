const VARIANTS = new Set(["match", "muted", "empty", "missing"]);

export default function SkillChip({ children, variant }) {
  const modifier = variant && VARIANTS.has(variant) ? ` signal-chip--${variant}` : "";
  return <span className={`signal-chip${modifier}`}>{children}</span>;
}

export function SkillChipList({ skills = [], limit, variant = "match", overflowVariant = "muted" }) {
  if (!skills.length) return null;
  const visible = limit ? skills.slice(0, limit) : skills;
  const overflow = limit && skills.length > limit ? skills.length - limit : 0;

  return (
    <div className="signal-chips">
      {visible.map((skill) => (
        <SkillChip key={skill} variant={variant === "default" ? undefined : variant}>
          {skill}
        </SkillChip>
      ))}
      {overflow > 0 && <SkillChip variant={overflowVariant}>+{overflow}</SkillChip>}
    </div>
  );
}
