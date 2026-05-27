import { profileToPayload } from "./profileFields.js";

export function profileFieldsDirty(current, baseline) {
  if (!baseline) return true;
  return JSON.stringify(profileToPayload(current)) !== JSON.stringify(profileToPayload(baseline));
}
