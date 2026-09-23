import { API_BASE } from "./config";

export type AgentTurn = {
  turn_id: string;
  caption: string;
  move: string;
  phase: string;
  expression: string;
  next: string;
  alert_id: string | null;
  slot_id: string | null;
  audio_url: string | null;
  visemes: { offset_ms: number; viseme_id: number }[];
  duration_ms: number;
  prosody: { rate: string; pitch: string; pause_after_ms: number };
};

export type SpeechConfigResponse = {
  stt_provider: "azure" | "browser";
  region: string | null;
  bcp47: string;
  silence_end_of_turn_ms: number;
  initial_silence_timeout_ms: number;
  low_confidence_threshold: number;
  token: string | null;
  expires_in_s: number | null;
  languages: Record<string, string>;
  note: string;
};

async function j<T>(path: string, init?: RequestInit): Promise<T> {
  const r = await fetch(`${API_BASE}${path}`, { headers: { "Content-Type": "application/json" }, ...init });
  if (!r.ok) throw new Error(`${r.status} ${await r.text()}`);
  return r.json();
}

export const api = {
  start: (setting: "ed" | "gp_booking", language: string, consent: { ai_disclosure: boolean; tone_adaptation: boolean; summary_to_clinician: boolean }, register: string) =>
    j<{ conversation_id: string; agent_turns: AgentTurn[]; phase: string; versions: Record<string, unknown> }>("/conversations", {
      method: "POST",
      body: JSON.stringify({ setting, language, consent, persona_register: register }),
    }),
  turn: (cid: string, transcript: string, prosody: Record<string, number>, asr?: Record<string, unknown> | null, interrupted_at_ms?: number) =>
    j<{ person_turn_id: string; agent_turns: AgentTurn[]; phase: string; language: string; language_switched: boolean; detected_tone: { label: string; stored: boolean }; alerts: any[] }>(
      `/conversations/${cid}/turns`,
      { method: "POST", body: JSON.stringify({ transcript, prosody, asr: asr || undefined, asr_confidence: (asr as any)?.confidence ?? undefined, interrupted_at_ms }) },
    ),
  speechConfig: (language: string, register: string) => j<SpeechConfigResponse>(`/speech/config?language=${encodeURIComponent(language)}&register=${encodeURIComponent(register)}`),
  speechToken: () => j<{ token: string; expires_in_s: number; region: string }>(`/speech/token`),
  conversation: (cid: string) => j<any>(`/conversations/${cid}`),
  handover: (cid: string) => j<any>(`/conversations/${cid}/handover`),
  codingDocument: (cid: string) => j<any>(`/conversations/${cid}/coding-document`),
  ask: (cid: string, question: string) => j<{ answer: string }>(`/conversations/${cid}/clinician-questions`, { method: "POST", body: JSON.stringify({ question }) }),
  attest: (cid: string, clinician: string, diagnosis_block: any, edits: any) =>
    j<any>(`/conversations/${cid}/attest`, { method: "POST", body: JSON.stringify({ clinician, diagnosis_block, edits }) }),
  exportAll: (cid: string) => j<any>(`/conversations/${cid}/export`),
  contentStatus: () => j<any>(`/content/status`),
  audioUrl: (path: string) => `${API_BASE}${path}`,
};
