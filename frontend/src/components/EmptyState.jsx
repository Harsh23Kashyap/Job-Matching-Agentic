import EmptyStateIllustration from "./EmptyStateIllustration.jsx";
import BackgroundPattern from "./BackgroundPattern.jsx";

export default function EmptyState({
  title,
  description,
  checklist = [],
  action,
  helperText,
  illustrationVariant = "ready",
  variant = "default",
  compact = false,
  checklistStyle = "todo",
  patternVariant,
}) {
  return (
    <div className={`empty-state-card empty-state-card--${variant}${compact ? " empty-state-card--compact" : ""}`}>
      {patternVariant && <BackgroundPattern variant={patternVariant} scope="inline" />}
      <div className="empty-state-card__body">
        <EmptyStateIllustration variant={illustrationVariant} />
        <h3>{title}</h3>
        <p>{description}</p>
        {checklist.length > 0 && (
          <ul className={`empty-checklist empty-checklist--${checklistStyle}`}>
            {checklist.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        )}
        {action && <div className="empty-state-action">{action}</div>}
        {helperText && <p className="empty-state-helper">{helperText}</p>}
      </div>
    </div>
  );
}

const PROFILE_CHECKLIST = [
  "Upload or enter resume details",
  "Add skills",
  "Set compensation and preferences",
];

export function ProfileNeededEmpty({ action }) {
  return (
    <EmptyState
      variant="profile"
      illustrationVariant="profile-needed"
      title="Profile needed"
      description="Upload your resume or enter your skills so we can find roles that fit."
      checklist={PROFILE_CHECKLIST}
      checklistStyle="todo"
      action={action}
    />
  );
}

export function JobsReadyEmpty({ action }) {
  return (
    <EmptyState
      variant="jobs"
      illustrationVariant="ready"
      title="Ready to find matches"
      description="Your profile is ready. Search roles matched to your skills and preferences."
      action={action}
    />
  );
}

export function NoMatchingRolesEmpty({ action }) {
  return (
    <EmptyState
      variant="no-results"
      illustrationVariant="no-results"
      title="No matching roles found"
      description="Try lowering the minimum match or updating your skills."
      compact
      action={action}
    />
  );
}

export function EmployerNoCandidatesEmpty({ action }) {
  return (
    <EmptyState
      variant="no-results"
      illustrationVariant="no-results"
      patternVariant="employer-empty"
      title="No candidates matched yet"
      description="Try broadening skills, lowering experience, or refreshing matches."
      compact
      action={action}
    />
  );
}

export function EmployerRolesEmpty({ action }) {
  return (
    <EmptyState
      variant="empty"
      illustrationVariant="employer-jobs"
      patternVariant="employer-empty"
      title="No roles posted yet"
      description="Create your first role to start matching candidates."
      action={action}
    />
  );
}
