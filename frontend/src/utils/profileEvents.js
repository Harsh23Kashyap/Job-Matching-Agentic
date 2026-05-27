export const PROFILE_UPDATED_EVENT = "jobmatch:profile-updated";
export const JOBS_UPDATED_EVENT = "jobmatch:jobs-updated";

export function notifyProfileUpdated() {
  window.dispatchEvent(new Event(PROFILE_UPDATED_EVENT));
}

export function notifyJobsUpdated() {
  window.dispatchEvent(new Event(JOBS_UPDATED_EVENT));
}
