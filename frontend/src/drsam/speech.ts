/**
 * Browser speech: synthesis (fallback when the API returns no audio) and recognition
 * (Web Speech API) with barge-in. Azure recognition lives in recognition.ts and uses
 * the same handler contract; this file is the fallback path.
 */
export function speechAvailable() {
  return typeof window !== "undefined" && "speechSynthesis" in window;
}

let voiceCache: Record<string, SpeechSynthesisVoice | null> = {};

function pickVoice(bcp47: string): SpeechSynthesisVoice | null {
  if (bcp47 in voiceCache) return voiceCache[bcp47];
  const voices = window.speechSynthesis?.getVoices?.() || [];
  const lang = bcp47.toLowerCase();
  const match = voices.find((v) => v.lang?.toLowerCase() === lang) || voices.find((v) => v.lang?.toLowerCase().startsWith(lang.split("-")[0]));
  voiceCache[bcp47] = match || null;
  return match || null;
}

export type SpeakHandle = { done: Promise<void>; cancel: () => void };

export function speakBrowser(text: string, bcp47: string, rate = 0.92, onBoundary?: (charIndex: number) => void): SpeakHandle {
  if (!speechAvailable() || !text.trim()) return { done: Promise.resolve(), cancel: () => {} };
  let finish!: () => void;
  const done = new Promise<void>((res) => (finish = res));
  let ended = false;
  const end = () => {
    if (ended) return;
    ended = true;
    finish();
  };
  try {
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    const v = pickVoice(bcp47);
    if (v) u.voice = v;
    u.lang = bcp47;
    u.rate = rate;
    u.onend = end;
    u.onerror = end;
    u.onboundary = (e) => onBoundary?.(e.charIndex);
    window.speechSynthesis.speak(u);
    setTimeout(end, Math.min(30000, 1500 + text.length * 75));
  } catch {
    end();
  }
  return { done, cancel: () => { window.speechSynthesis.cancel(); end(); } };
}

export function playAudio(url: string): SpeakHandle {
  const audio = new Audio(url);
  let finish!: () => void;
  const done = new Promise<void>((res) => (finish = res));
  audio.onended = () => finish();
  audio.onerror = () => finish();
  audio.play().catch(() => finish());
  return { done, cancel: () => { audio.pause(); finish(); } };
}

export type Recognizer = {
  start: () => void;
  stop: () => void;
  available: boolean;
};

export function makeRecognizer(bcp47: string, handlers: { onStart?: () => void; onInterim?: (t: string) => void; onFinal: (t: string, confidence: number, durationMs: number) => void; onError?: (e: string) => void }, endOfTurnMs = 1200): Recognizer {
  const Ctor = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!Ctor) return { start: () => {}, stop: () => {}, available: false };
  const rec = new Ctor();
  rec.lang = bcp47;
  rec.interimResults = true;
  rec.continuous = true;
  let startedAt = 0;
  let finalText = "";
  let confidences: number[] = [];
  let silenceTimer: number | null = null;
  let wanted = false;
  let announced = false;
  const flush = () => {
    if (!finalText.trim()) return;
    const t = finalText.trim();
    finalText = "";
    const conf = confidences.length ? confidences.reduce((a, b) => a + b, 0) / confidences.length : 0;
    confidences = [];
    handlers.onFinal(t, conf, Date.now() - startedAt);
    startedAt = Date.now();
  };
  rec.onstart = () => { startedAt = Date.now(); if (!announced) { announced = true; handlers.onStart?.(); } };
  rec.onresult = (e: any) => {
    let interim = "";
    for (let i = e.resultIndex; i < e.results.length; i++) {
      const r = e.results[i];
      if (r.isFinal) { finalText += " " + r[0].transcript; confidences.push(r[0].confidence || 0); }
      else interim += r[0].transcript;
    }
    handlers.onInterim?.((finalText + " " + interim).trim());
    if (silenceTimer) window.clearTimeout(silenceTimer);
    // end-of-utterance: the configured silence with no new results (N-3)
    silenceTimer = window.setTimeout(flush, endOfTurnMs);
  };
  rec.onerror = (e: any) => {
    // "no-speech" and "aborted" are routine in ambient listening; the session restarts below
    if (e.error === "no-speech" || e.error === "aborted") return;
    handlers.onError?.(e.error || "speech error");
  };
  // ambient listening: the browser ends a session after a stretch of silence; keep it open until stopped
  rec.onend = () => { flush(); if (wanted) window.setTimeout(() => { if (wanted) { try { rec.start(); } catch {} } }, 250); };
  return {
    start: () => { wanted = true; try { rec.start(); } catch {} },
    stop: () => { wanted = false; try { rec.stop(); } catch {} },
    available: true,
  };
}
