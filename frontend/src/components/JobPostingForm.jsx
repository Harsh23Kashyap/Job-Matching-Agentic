import FormField from "./FormField.jsx";
import SkillsChipsInput from "./SkillsChipsInput.jsx";
import ExperienceInput from "./ExperienceInput.jsx";
import BudgetRangeInput from "./BudgetRangeInput.jsx";
import CustomCheckbox from "./CustomCheckbox.jsx";
import { JOB_DESCRIPTION_MAX } from "../utils/jobFields.js";

const DESCRIPTION_PLACEHOLDER =
  "Example: We're looking for a backend engineer to build APIs and data pipelines. You'll work with Python, collaborate with product, and help scale services used by thousands of customers.";

export default function JobPostingForm({ fields, errors = {}, onChange, footer }) {
  const descLen = fields.description?.length ?? 0;

  return (
    <div className="job-posting-form-wrap">
      <div className="profile-form-fields">
        <div className="profile-form-section">
          <h3 className="profile-form-section-title">Role basics</h3>
          <p className="profile-form-section-helper">Core details candidates see first when browsing matches.</p>

          <FormField label="Title" helper="Use a clear role name, e.g. Senior Backend Engineer." error={errors.title} htmlFor="ej-title">
            <input
              id="ej-title"
              placeholder="Machine Learning Engineer"
              value={fields.title}
              onChange={(e) => onChange({ ...fields, title: e.target.value })}
              required
            />
          </FormField>

          <div className="form-row-2">
            <FormField label="Company" helper="Your organization or team name." htmlFor="ej-company">
              <input
                id="ej-company"
                placeholder="Acme Labs"
                value={fields.company}
                onChange={(e) => onChange({ ...fields, company: e.target.value })}
              />
            </FormField>
            <FormField label="Location" helper="City, region, or Hybrid." htmlFor="ej-location">
              <input
                id="ej-location"
                placeholder="Bengaluru · Hybrid"
                value={fields.location}
                onChange={(e) => onChange({ ...fields, location: e.target.value })}
              />
            </FormField>
          </div>
        </div>

        <div className="profile-form-section">
          <h3 className="profile-form-section-title">Skills & experience</h3>
          <p className="profile-form-section-helper">List must-have skills and the minimum experience level.</p>

          <FormField
            label="Required skills"
            helper="Add skills one at a time or paste a comma-separated list."
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
        </div>

        <div className="profile-form-section">
          <h3 className="profile-form-section-title">Compensation</h3>
          <FormField
            label="Compensation budget"
            helper="Annual compensation budget for this role."
            error={errors.budget_min || errors.budget_max}
            htmlFor="job-budget-min"
          >
            <BudgetRangeInput
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
        </div>

        <div className="profile-form-section">
          <h3 className="profile-form-section-title">Work setup</h3>
          <CustomCheckbox
            id="ej-remote"
            label="Remote allowed"
            helper="Candidates open to remote work can match with this role."
            checked={fields.remote_policy}
            onChange={(remote_policy) => onChange({ ...fields, remote_policy })}
          />
        </div>

        <div className="profile-form-section">
          <h3 className="profile-form-section-title">Description</h3>
          <p className="profile-form-section-helper">Summarize responsibilities, team context, and what success looks like.</p>

          <FormField label="Description" error={errors.description} htmlFor="ej-desc">
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
        </div>
      </div>

      {footer}
    </div>
  );
}
