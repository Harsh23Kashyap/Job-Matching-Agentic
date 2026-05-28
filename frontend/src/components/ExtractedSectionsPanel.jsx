import {
  formatEducationEntry,
  formatProjectEntry,
  hasExtractedSections,
} from "../utils/extractedSections.js";

export default function ExtractedSectionsPanel({ extracted = {} }) {
  const data = extracted ?? {};
  if (!hasExtractedSections(data)) return null;

  const education = (data.education || []).map(formatEducationEntry).filter(Boolean);
  const projects = (data.projects || []).map(formatProjectEntry).filter(Boolean);
  const responsibilities = (data.responsibilities || []).filter(Boolean);
  const educationRequirements = (data.education_requirements || []).filter(Boolean);

  return (
    <section className="extracted-sections-panel portal-panel portal-panel--elevated">
      <h3 className="extracted-sections-panel__title">Parsed sections</h3>
      <p className="form-helper extracted-sections-panel__intro">
        Pulled from your document. Summary and skills above are prefilled; education and projects are shown here for review.
      </p>
      {education.length > 0 && (
        <div className="extracted-sections-panel__block">
          <h4>Education</h4>
          <ul>
            {education.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      )}
      {projects.length > 0 && (
        <div className="extracted-sections-panel__block">
          <h4>Projects</h4>
          <ul>
            {projects.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      )}
      {responsibilities.length > 0 && (
        <div className="extracted-sections-panel__block">
          <h4>Responsibilities</h4>
          <ul>
            {responsibilities.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      )}
      {educationRequirements.length > 0 && (
        <div className="extracted-sections-panel__block">
          <h4>Education requirements</h4>
          <ul>
            {educationRequirements.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
