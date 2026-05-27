export default function RemotePolicyField({ id, checked, onChange }) {
  return (
    <fieldset className="remote-policy-field">
      <legend className="remote-policy-field__legend">Remote work</legend>
      <p className="form-helper remote-policy-field__helper">
        Whether remote-preference candidates can match this role.
      </p>
      <div className="remote-policy-field__options">
        <button
          type="button"
          id={`${id}-onsite`}
          className={`remote-policy-option${!checked ? " remote-policy-option--active" : ""}`}
          aria-pressed={!checked}
          onClick={() => onChange(false)}
        >
          <span className="remote-policy-option__title">On-site / hybrid</span>
          <span className="remote-policy-option__desc">In-office or hybrid.</span>
        </button>
        <button
          type="button"
          id={id}
          className={`remote-policy-option${checked ? " remote-policy-option--active" : ""}`}
          aria-pressed={checked}
          onClick={() => onChange(true)}
        >
          <span className="remote-policy-option__title">Remote allowed</span>
          <span className="remote-policy-option__desc">Remote and remote-friendly candidates can match.</span>
        </button>
      </div>
    </fieldset>
  );
}
