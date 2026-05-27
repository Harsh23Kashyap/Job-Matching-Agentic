import FormField from "./FormField.jsx";
import FormSection from "./FormSection.jsx";
import CompensationInput from "./CompensationInput.jsx";
import ExperienceInput from "./ExperienceInput.jsx";
import CustomCheckbox from "./CustomCheckbox.jsx";
import SkillsChipsInput from "./SkillsChipsInput.jsx";
import LinksChipsInput from "./LinksChipsInput.jsx";
import { SUMMARY_MAX } from "../utils/validation.js";

export default function ProfileForm({
  fields,
  errors = {},
  onChange,
  footer,
  requireSkills = false,
}) {
  return (
    <div className="portal-form-wrap">
      <div className="portal-form-fields">
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

        <FormSection
          title="Contact & links"
          helper="How employers can reach you. These fields are filled from your resume when possible — edit anything that looks off."
        >
          <FormField
            label="Email"
            helper="Work or personal email. We'll never share it without your consent."
            error={errors.email}
            htmlFor="pf-email"
          >
            <input
              id="pf-email"
              type="email"
              autoComplete="email"
              placeholder="you@example.com"
              value={fields.email}
              onChange={(e) => onChange({ ...fields, email: e.target.value })}
            />
          </FormField>

          <FormField
            label="Phone"
            helper="Include country code for numbers outside your home region (e.g. +91 98765 43210)."
            error={errors.phone}
            htmlFor="pf-phone"
          >
            <input
              id="pf-phone"
              type="tel"
              autoComplete="tel"
              placeholder="+91 98765 43210"
              value={fields.phone}
              onChange={(e) => onChange({ ...fields, phone: e.target.value })}
            />
          </FormField>

          <FormField
            label="LinkedIn"
            helper="Full profile URL — we'll add https:// if you paste linkedin.com/in/…"
            error={errors.linkedin}
            htmlFor="pf-linkedin"
          >
            <input
              id="pf-linkedin"
              type="url"
              placeholder="https://linkedin.com/in/your-handle"
              value={fields.linkedin}
              onChange={(e) => onChange({ ...fields, linkedin: e.target.value })}
            />
          </FormField>

          <FormField
            label="Portfolio or website"
            helper="GitHub, personal site, or portfolio — shown to employers reviewing your profile."
            error={errors.portfolio}
            htmlFor="pf-portfolio"
          >
            <input
              id="pf-portfolio"
              type="url"
              placeholder="https://github.com/you or your personal site"
              value={fields.portfolio}
              onChange={(e) => onChange({ ...fields, portfolio: e.target.value })}
            />
          </FormField>

          <FormField
            label="Other links"
            helper="GitLab, Medium, project demos, or anything else worth sharing."
            error={errors.other_links}
            htmlFor="pf-other-links"
          >
            <LinksChipsInput
              id="pf-other-links"
              value={fields.other_links || []}
              onChange={(links) => onChange({ ...fields, other_links: links })}
              error={errors.other_links}
            />
          </FormField>
        </FormSection>

        <FormField
          label="Skills"
          helper="Type a skill and press Enter, or paste a comma-separated list. Remove chips you don't want."
          error={errors.skills}
          htmlFor="pf-skills"
        >
          <SkillsChipsInput
            id="pf-skills"
            value={fields.skills}
            onChange={(v) => onChange({ ...fields, skills: v })}
            error={errors.skills}
            required={requireSkills}
          />
        </FormField>

        <FormField
          label="Years of experience"
          helper="Use your total professional experience. Internships are optional."
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
          label="Expected annual total compensation"
          helper="Optional. Total package per year — base, bonus, equity, and recurring pay. Pick a currency, then enter a whole number."
          error={errors.preferred_salary}
          htmlFor="pf-salary"
          optional
        >
          <CompensationInput
            id="pf-salary"
            amount={fields.preferred_salary}
            currency={fields.preferred_currency || "INR"}
            onAmountChange={(v) => onChange({ ...fields, preferred_salary: v ?? "" })}
            onCurrencyChange={(v) => onChange({ ...fields, preferred_currency: v })}
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
          helper="Two or three sentences on your focus areas — this appears on match cards for employers."
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
      {footer && <div className="portal-form-footer">{footer}</div>}
    </div>
  );
}
