export const API_BASE = (window.__AIDOC_CONFIG__?.apiBaseUrl || "/api").replace(/\/$/, "");
export const LANGUAGES: Record<string, { name: string; bcp47: string }> = {
  en: { name: "English", bcp47: "en-AU" },
  vi: { name: "Tiếng Việt", bcp47: "vi-VN" },
  it: { name: "Italiano", bcp47: "it-IT" },
  fr: { name: "Français", bcp47: "fr-FR" },
  ms: { name: "Bahasa Melayu", bcp47: "ms-MY" },
  hi: { name: "हिन्दी", bcp47: "hi-IN" },
};
