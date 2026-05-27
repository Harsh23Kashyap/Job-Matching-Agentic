import EmptyStateIllustration from "./EmptyStateIllustration.jsx";
import BackgroundOrnaments from "./BackgroundOrnaments.jsx";

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
      {patternVariant && <BackgroundOrnaments variant={patternVariant} scope="inline" />}
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
  "Upload or paste resume details",
  "Add skills",
  "Set pay and work preferences",
];

export function ProfileNeededEmpty({ action }) {
  return (
    <EmptyState
      variant="profile"
      illustrationVariant="profile-needed"
      patternVariant="profile"
      title="Set up your profile"
      description="Add your resume or skills so we can rank roles for you."
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
      illustrationVariant="jobs-search"
      patternVariant="jobs"
      title="Find roles matched to your profile"
      description="Your profile is saved. Start a match search to see ranked openings."
      action={action}
      helperText="No search has been run yet"
    />
  );
}

export function NoMatchingRolesEmpty({ action, filteredOut = false }) {
  return (
    <EmptyState
      variant="no-results"
      illustrationVariant="no-results"
      title={filteredOut ? "No roles pass your filters" : "No roles matched"}
      description={
        filteredOut
          ? "Your search returned matches, but filters hide them. Lower the minimum match or clear Remote only."
          : "No roles in the corpus matched your profile yet. Update your skills or try again later."
      }
      compact
      action={action}
    />
  );
}

export function ProfileIncompleteEmpty({ action }) {
  return (
    <EmptyState
      variant="profile"
      illustrationVariant="profile-needed"
      patternVariant="profile"
      title="Finish your profile"
      description="We found a profile on your account, but it still needs a name before you can search for roles."
      action={action}
    />
  );
}

export function ProfileStaleEmpty({ action }) {
  return (
    <EmptyState
      variant="profile"
      illustrationVariant="profile-needed"
      patternVariant="profile"
      title="Restore your profile"
      description="Your account is linked to a profile that is no longer loaded. Re-save your details on the Profile page to search for roles again."
      action={action}
    />
  );
}

export function EmployerAllClosedEmpty({ action }) {
  return (
    <EmptyState
      variant="jobs"
      illustrationVariant="employer-jobs"
      title="No open roles"
      description="You have closed roles on file. Post a new open role or reopen one from My jobs."
      compact
      action={action}
    />
  );
}

export function EmployerCandidatesReadyEmpty({ action, jobTitle }) {
  return (
    <EmptyState
      variant="jobs"
      illustrationVariant="ready"
      title="Review candidates"
      description={
        jobTitle
          ? `Refresh matches to load candidates ranked for ${jobTitle}.`
          : "Choose a role and refresh matches to load ranked candidates."
      }
      action={action}
      helperText="Ranking uses skills, experience, and profile fit."
    />
  );
}

export function EmployerNoCandidatesEmpty({ action }) {
  return (
    <EmptyState
      variant="no-results"
      illustrationVariant="no-results"
      title="No candidates matched"
      description="Widen required skills, lower experience, or refresh matches."
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
      patternVariant="employer-jobs"
      title="No roles posted"
      description="Post a role to start matching candidates."
      checklist={[
        "Import a JD or enter role details",
        "Add skills, experience, and pay range",
        "Publish and review matches",
      ]}
      checklistStyle="todo"
      action={action}
      helperText="Use the form on the right, or paste a job description to fill it in."
    />
  );
}

export function ActivePostingsEmpty({ action }) {
  return (
    <EmptyState
      variant="jobs"
      illustrationVariant="employer-jobs"
      title="No open roles"
      description="Every role is closed. Post a new one to match candidates again."
      compact
      action={action}
      helperText="Closed roles stay in the list below for review and edits."
    />
  );
}
