export const PROFILE_QUALITY_GRADES = {
  strong: "Strong profile",
  good: "Good profile",
  fair: "Fair — room to improve",
  needs_work: "Needs work",
};

export function profileQualityGradeLabel(grade) {
  if (!grade) return null;
  return PROFILE_QUALITY_GRADES[grade] || grade.replace(/_/g, " ");
}
