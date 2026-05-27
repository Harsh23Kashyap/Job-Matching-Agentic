import FormField from "./FormField.jsx";
import FormSection from "./FormSection.jsx";
import SkillsChipsInput from "./SkillsChipsInput.jsx";
import ExperienceInput from "./ExperienceInput.jsx";
import CompensationInput from "./CompensationInput.jsx";
import RemotePolicyField from "./RemotePolicyField.jsx";
import { JOB_DESCRIPTION_MAX, JOB_TYPE_OPTIONS } from "../utils/jobFields.js";

const DESCRIPTION_PLACEHOLDER =
  "Role overview, day-to-day work, must-haves, and what good looks like in the first 90 days.";

export default function JobPostingForm({ fields, errors = {}, onChange, footer }) {
  const descLen = fields.description?.length ?? 0;
  const descWarn = descLen > JOB_DESCRIPTION_MAX * 0.9;

  return (
    <div className="portal-form-wrap employer-job-form-wrap">
      <div className="portal-form-fields employer-job-form-fields">
        <FormSection
          title="Role basics"
          helper="Shown to candidates in search and match results."
        >
          <FormField
            label="Job title"
            helper="Clear, searchable title (e.g. Senior Backend Engineer)."
            error={errors.title}
            htmlFor="ej-title"
          >
            <input
              id="ej-title"
              placeholder="Senior Machine Learning Engineer"
              value={fields.title}
              onChange={(e) => onChange({ ...fields, title: e.target.value })}
              required
            />
          </FormField>

          <FormField
            label="Company"
            helper="Company or team name on the posting."
            error={errors.company}
            htmlFor="ej-company"
          >
            <input
              id="ej-company"
              placeholder="Acme Labs"
              value={fields.company}
              onChange={(e) => onChange({ ...fields, company: e.target.value })}
            />
          </FormField>
        </FormSection>

        <FormSection title="Work setup" helper="Location, employment type, and remote policy.">
          <div className="form-row-2 employer-work-setup-row">
            <FormField
              label="Location"
              helper="City, region, or Hybrid."
              htmlFor="ej-location"
            >
              <input
                id="ej-location"
                placeholder="Bengaluru · Hybrid"
                value={fields.location}
                onChange={(e) => onChange({ ...fields, location: e.target.value })}
              />
            </FormField>
            <FormField label="Employment type" helper="Full-time, contract, etc." htmlFor="ej-job-type">
              <select
                id="ej-job-type"
                className="portal-select"
                value={fields.job_type}
                onChange={(e) => onChange({ ...fields, job_type: e.target.value })}
              >
                <option value="">Select type</option>
                {JOB_TYPE_OPTIONS.filter(Boolean).map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </FormField>
          </div>

          <RemotePolicyField
            id="ej-remote"
            checked={fields.remote_policy}
            onChange={(remote_policy) => onChange({ ...fields, remote_policy })}
          />
        </FormSection>

        <FormSection
          title="Requirements"
          helper="Used to rank candidate matches."
        >
          <FormField
            label="Required skills"
            helper="Enter after each skill, or paste comma-separated values."
            error={errors.required_skills}
            htmlFor="ej-skills"
          >
            <SkillsChipsInput
              id="ej-skills"
              value={fields.required_skills}
              onChange={(value) => onChange({ ...fields, required_skills: value })}
              error={errors.required_skills}
            />
          </FormField>

          <FormField
            label="Minimum experience"
            helper="Minimum years of relevant experience."
            error={errors.required_experience}
            htmlFor="ej-exp"
          >
            <ExperienceInput
              id="ej-exp"
              value={fields.required_experience}
              onChange={(value) => onChange({ ...fields, required_experience: value })}
              error={errors.required_experience}
            />
          </FormField>
        </FormSection>

        <FormSection
          title="Total compensation"
          helper="Annual total comp range offered for this role."
        >
          <FormField
            label="Budget range"
            helper="Currency, then min and max per year."
            error={errors.budget_min || errors.budget_max}
            htmlFor="job-budget-min"
          >
            <CompensationInput
              id="job-budget"
              mode="range"
              currency={fields.budget_currency}
              minAmount={fields.budget_min}
              maxAmount={fields.budget_max}
              onCurrencyChange={(budget_currency) => onChange({ ...fields, budget_currency })}
              onMinChange={(budget_min) => onChange({ ...fields, budget_min })}
              onMaxChange={(budget_max) => onChange({ ...fields, budget_max })}
              minError={errors.budget_min}
              maxError={errors.budget_max}
            />
          </FormField>
        </FormSection>

        <FormSection
          title="Role description"
          helper="Full posting: responsibilities, team, benefits if you list them."
        >
          <FormField label="Description" error={errors.description} htmlFor="ej-desc">
            <textarea
              id="ej-desc"
              className="job-description-textarea"
              rows={9}
              placeholder={DESCRIPTION_PLACEHOLDER}
              value={fields.description}
              onChange={(e) => onChange({ ...fields, description: e.target.value })}
              maxLength={JOB_DESCRIPTION_MAX}
              aria-describedby="ej-desc-count"
            />
            <p
              id="ej-desc-count"
              className={`char-count${descWarn ? " char-count--warn" : ""}`}
            >
              {descLen.toLocaleString()} / {JOB_DESCRIPTION_MAX.toLocaleString()} characters
            </p>
          </FormField>
        </FormSection>
      </div>

      {footer}
    </div>
  );
}
