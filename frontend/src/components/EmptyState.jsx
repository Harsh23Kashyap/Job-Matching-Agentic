import JobsEmptyIllustration from "./JobsEmptyIllustration.jsx";

export default function EmptyState({
  title,
  description,
  checklist = [],
  action,
  helperText,
  illustration,
  variant = "default",
}) {
  return (
    <div className={`empty-state-card empty-state-card--${variant}`}>
      {illustration || null}
      <h3>{title}</h3>
      <p>{description}</p>
      {checklist.length > 0 && (
        <ul className="empty-checklist">
          {checklist.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      )}
      {action && <div className="empty-state-action">{action}</div>}
      {helperText && <p className="empty-state-helper">{helperText}</p>}
    </div>
  );
}

export function ProfileNeededEmpty({ action }) {
  return (
    <EmptyState
      variant="profile"
      title="Profile needed"
      description="Upload your resume or enter your skills so we can find roles that fit."
      action={action}
      helperText="A complete profile unlocks personalized match rankings."
    />
  );
}

export function JobsReadyEmpty({ action }) {
  return (
    <EmptyState
      variant="jobs"
      illustration={<JobsEmptyIllustration />}
      title="Ready to find matches"
      description="Your profile is complete. Search roles matched to your skills and preferences."
      action={action}
      helperText="We'll rank open roles by skills, experience, and compensation fit."
    />
  );
}
