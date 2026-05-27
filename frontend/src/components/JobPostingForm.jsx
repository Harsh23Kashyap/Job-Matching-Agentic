import FormField from "./FormField.jsx";
import FormSection from "./FormSection.jsx";
import SkillsChipsInput from "./SkillsChipsInput.jsx";
import ExperienceInput from "./ExperienceInput.jsx";
import CompensationInput from "./CompensationInput.jsx";
import CustomCheckbox from "./CustomCheckbox.jsx";
import { JOB_DESCRIPTION_MAX, JOB_TYPE_OPTIONS } from "../utils/jobFields.js";

const DESCRIPTION_PLACEHOLDER =
  "Example: We're looking for a backend engineer to build APIs and data pipelines. You'll work with Python, collaborate with product, and help scale services used by thousands of customers.";

export default function JobPostingForm({ fields, errors = {}, onChange, footer }) {
  const descLen = fields.description?.length ?? 0;

  return (
    <div className="portal-form-wrap employer-job-form-wrap">
      <div className="portal-form-fields">
        <FormSection
          title="Role basics"
          helper="Core details candidates see first when browsing matches."
        >
          <FormField label="Title" helper="Use a clear role name, e.g. Senior Backend Engineer." error={errors.title} htmlFor="ej-title">
            <input
              id="ej-title"
              placeholder="Machine Learning Engineer"
              value={fields.title}
              onChange={(e) => onChange({ ...fields, title: e.target.value })}
              required
            />
          </FormField>

          <FormField label="Company" helper="Your organization or team name." htmlFor="ej-company">
            <input
              id="ej-company"
              placeholder="Acme Labs"
              value={fields.company}
              onChange={(e) => onChange({ ...fields, company: e.target.value })}
            />
          </FormField>
        </FormSection>

        <FormSection
          title="Work setup"
          helper="Location, employment type, and remote policy for this role."
        >
          <div className="form-row-2 employer-work-setup-row">
            <FormField label="Location" helper="City, region, or Hybrid." htmlFor="ej-location">
              <input
                id="ej-location"
                placeholder="Bengaluru · Hybrid"
                value={fields.location}
                onChange={(e) => onChange({ ...fields, location: e.target.value })}
              />
            </FormField>
            <FormField label="Job type" helper="Employment type for this posting." htmlFor="ej-job-type">
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

          <CustomCheckbox
            id="ej-remote"
            label="Remote allowed"
            helper="Candidates open to remote work can match with this role."
            checked={fields.remote_policy}
            onChange={(remote_policy) => onChange({ ...fields, remote_policy })}
          />
        </FormSection>

        <FormSection
          title="Skills & experience"
          helper="List must-have skills and the minimum experience level."
        >
          <FormField
            label="Required skills"
            helper="Press Enter after each skill, or paste a comma-separated list."
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
            label="Required experience"
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
          helper="Annual total compensation range offered for this role."
        >
          <FormField
            label="Compensation range"
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
          title="Description"
          helper="Summarize responsibilities, team context, and what success looks like."
        >
          <FormField label="Role description" error={errors.description} htmlFor="ej-desc">
            <textarea
              id="ej-desc"
              className="job-description-textarea"
              rows={8}
              placeholder={DESCRIPTION_PLACEHOLDER}
              value={fields.description}
              onChange={(e) => onChange({ ...fields, description: e.target.value })}
              maxLength={JOB_DESCRIPTION_MAX}
            />
            <p className={`char-count${descLen > JOB_DESCRIPTION_MAX * 0.9 ? " char-count--warn" : ""}`}>
              {descLen} / {JOB_DESCRIPTION_MAX}
            </p>
          </FormField>
        </FormSection>
      </div>

      {footer}
    </div>
  );
}
