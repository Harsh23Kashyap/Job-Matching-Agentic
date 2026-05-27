import { Link } from "react-router-dom";
import { IconEmpty } from "./icons.jsx";

export default function EmptyState({ title, description, checklist = [], action }) {
  return (
    <div className="empty-state-product">
      <IconEmpty />
      <h3>{title}</h3>
      <p>{description}</p>
      {checklist.length > 0 && (
        <ul className="empty-checklist">
          {checklist.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      )}
      {action}
    </div>
  );
}

export function ProfileEmptyState() {
  return (
    <EmptyState
      title="No matches yet"
      description="Complete your profile so we can compare your skills with open roles."
      checklist={[
        "Upload or enter resume details",
        "Add skills",
        "Set preferences",
      ]}
      action={<Link to="/candidate/onboarding" className="btn-primary">Set up profile</Link>}
    />
  );
}
