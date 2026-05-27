import FormField from "./FormField.jsx";
import SalaryInput from "./SalaryInput.jsx";
import ExperienceInput from "./ExperienceInput.jsx";
import CustomCheckbox from "./CustomCheckbox.jsx";
import { SUMMARY_MAX } from "../utils/validation.js";

export default function ProfileForm({
  fields,
  errors = {},
  onChange,
  footer,
  requireSkills = false,
}) {
  return (
    <div className="profile-form-wrap">
      <div className="profile-form-fields">
        <FormField
          label="Name"
          helper="Use your full name as shown on your resume."
          error={errors.name}
          htmlFor="pf-name"
        >
          <input
            id="pf-name"
            value={fields.name}
            onChange={(e) => onChange({ ...fields, name: e.target.value })}
            required
          />
        </FormField>

        <FormField
          label="Skills"
          helper="Separate skills with commas. Example: Java, Spring Boot, Python, AWS"
          error={errors.skills}
          htmlFor="pf-skills"
        >
          <input
            id="pf-skills"
            value={fields.skills}
            onChange={(e) => onChange({ ...fields, skills: e.target.value })}
            required={requireSkills}
          />
        </FormField>

        <FormField
          label="Years of experience"
          helper="Use total professional experience. Internships optional."
          error={errors.experience_years}
          htmlFor="pf-exp"
        >
          <ExperienceInput
            id="pf-exp"
            value={fields.experience_years}
            onChange={(v) => onChange({ ...fields, experience_years: v })}
            error={errors.experience_years}
          />
        </FormField>

        <FormField
          label="Preferred salary"
          helper="Annual salary expectation in INR."
          error={errors.preferred_salary}
          htmlFor="pf-salary"
        >
          <SalaryInput
            id="pf-salary"
            value={fields.preferred_salary}
            onChange={(v) => onChange({ ...fields, preferred_salary: v ?? "" })}
            error={errors.preferred_salary}
          />
        </FormField>

        <CustomCheckbox
          id="pf-remote"
          checked={fields.remote_preference}
          onChange={(v) => onChange({ ...fields, remote_preference: v })}
          label="Open to remote work"
          helper="We'll include remote-friendly roles in your matches."
        />

        <FormField
          label="Summary"
          helper="A short overview for employers."
          error={errors.summary}
          htmlFor="pf-summary"
        >
          <textarea
            id="pf-summary"
            rows={4}
            maxLength={SUMMARY_MAX}
            placeholder="Example: Backend engineer with experience in Java, Spring Boot, distributed systems, and AI tooling."
            value={fields.summary}
            onChange={(e) => onChange({ ...fields, summary: e.target.value })}
          />
          <span className="char-count">
            {(fields.summary || "").length}/{SUMMARY_MAX} characters
          </span>
        </FormField>
      </div>
      {footer && <div className="profile-form-footer">{footer}</div>}
    </div>
  );
}
