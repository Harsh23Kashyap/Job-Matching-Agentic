const SECTIONS = [
  { id: "admin-section-health", label: "Health" },
  { id: "admin-section-system", label: "System" },
  { id: "admin-section-activity", label: "Activity" },
  { id: "admin-section-fairness", label: "Fairness" },
  { id: "admin-section-matching", label: "Matching" },
];

export default function AdminSectionNav() {
  const scrollTo = (id) => {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <nav className="admin-section-nav" aria-label="Admin sections">
      {SECTIONS.map((section) => (
        <button key={section.id} type="button" className="admin-section-nav__link" onClick={() => scrollTo(section.id)}>
          {section.label}
        </button>
      ))}
    </nav>
  );
}
