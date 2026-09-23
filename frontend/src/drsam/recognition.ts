/**
 * Speech recognition for the patient's side. Azure AI Speech runs in the browser
 * with a short-lived token from the API (the key never reaches the browser); the
 * Web Speech API is the fallback. Both expose the same handler contract.
 *
 * N-1 barge-in: the caller stops Dr Sam on the first partial result.
 * N-3 endpointing: the segmentation silence comes from the deployment parameters
 *     (longer for the older register), never the vendor default.
 * N-9 confidence: every final result carries the recogniser's per-utterance
 *     confidence, which travels with the turn to the transcript layer.
 */
import { api, SpeechConfigResponse } from "../api";
import { makeRecognizer, Recognizer } from "./speech";

export type AsrDetail = {
  provider: "azure" | "browser";
  confidence: number | null;
  language: string;
  duration_ms: number;
  offset_ms?: number;
  nbest?: { text: string; confidence: number }[];
  segments: number;
  endpoint_silence_ms: number;
};

export type RecognitionHandlers = {
  onStart?: () => void;
  onInterim?: (text: string) => void;
  onFinal: (text: string, asr: AsrDetail, prosody: { words_per_minute: number; duration_ms: number; word_count: number }) => void;
  onError?: (message: string) => void;
};

function prosodyFor(text: string, durationMs: number) {
  const words = text.split(/\s+/).filter(Boolean).length;
  const wpm = durationMs > 0 ? Math.round((words / durationMs) * 60000) : 0;
  return { words_per_minute: wpm, duration_ms: durationMs, word_count: words };
}

/** The browser recogniser wrapped in the shared contract. */
function browserRecognizer(cfg: SpeechConfigResponse, handlers: RecognitionHandlers): Recognizer {
  return makeRecognizer(cfg.bcp47, {
    onStart: handlers.onStart,
    onInterim: handlers.onInterim,
    onFinal: (t, conf, dur) =>
      handlers.onFinal(t, { provider: "browser", confidence: conf || null, language: cfg.bcp47, duration_ms: dur, segments: 1, endpoint_silence_ms: cfg.silence_end_of_turn_ms }, prosodyFor(t, dur)),
    onError: handlers.onError,
  }, cfg.silence_end_of_turn_ms);
}

/** Azure AI Speech in the browser. Continuous recognition; a turn ends on the configured silence. */
async function azureRecognizer(cfg: SpeechConfigResponse, handlers: RecognitionHandlers): Promise<Recognizer> {
  const sdk = await import("microsoft-cognitiveservices-speech-sdk");
  const speechConfig = sdk.SpeechConfig.fromAuthorizationToken(cfg.token!, cfg.region!);
  speechConfig.speechRecognitionLanguage = cfg.bcp47;
  speechConfig.outputFormat = sdk.OutputFormat.Detailed;
  // N-3: a pause shorter than this is not the end of the turn; slow speakers are not cut off
  speechConfig.setProperty(sdk.PropertyId.Speech_SegmentationSilenceTimeoutMs, String(cfg.silence_end_of_turn_ms));
  speechConfig.setProperty(sdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, String(cfg.silence_end_of_turn_ms));
  speechConfig.setProperty(sdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, String(cfg.initial_silence_timeout_ms));
  speechConfig.enableDictation();
  const audio = sdk.AudioConfig.fromDefaultMicrophoneInput();
  const rec = new sdk.SpeechRecognizer(speechConfig, audio);

  let finalText = "";
  let confidences: number[] = [];
  let nbest: { text: string; confidence: number }[] = [];
  let segments = 0;
  let startedAt = Date.now();
  let firstOffsetMs: number | undefined;
  let flushTimer: number | null = null;
  let refreshTimer: number | null = null;

  const flush = () => {
    if (!finalText.trim()) return;
    const text = finalText.trim();
    const conf = confidences.length ? confidences.reduce((a, b) => a + b, 0) / confidences.length : null;
    const detail: AsrDetail = {
      provider: "azure", confidence: conf === null ? null : Math.round(conf * 1000) / 1000, language: cfg.bcp47,
      duration_ms: Date.now() - startedAt, offset_ms: firstOffsetMs, nbest: nbest.slice(0, 3), segments, endpoint_silence_ms: cfg.silence_end_of_turn_ms,
    };
    finalText = ""; confidences = []; nbest = []; segments = 0; firstOffsetMs = undefined;
    handlers.onFinal(text, detail, prosodyFor(text, detail.duration_ms));
    startedAt = Date.now();
  };

  rec.recognizing = (_s, e) => {
    if (e.result?.text) handlers.onInterim?.((finalText + " " + e.result.text).trim());
  };
  rec.recognized = (_s, e) => {
    if (e.result.reason !== sdk.ResultReason.RecognizedSpeech || !e.result.text) return;
    segments += 1;
    finalText += " " + e.result.text;
    try {
      const detailed = JSON.parse(e.result.json || "{}");
      const best = (detailed.NBest || []) as { Display?: string; Confidence?: number }[];
      if (best.length) {
        confidences.push(Number(best[0].Confidence ?? 0));
        nbest = best.slice(0, 3).map((b) => ({ text: b.Display || "", confidence: Number(b.Confidence ?? 0) }));
      }
      if (firstOffsetMs === undefined && typeof detailed.Offset === "number") firstOffsetMs = Math.round(detailed.Offset / 10000);
    } catch { /* detailed JSON absent: confidence stays unknown rather than invented */ }
    handlers.onInterim?.(finalText.trim());
    if (flushTimer) window.clearTimeout(flushTimer);
    // the service already waited the segmentation silence before this result; a short grace joins run-on sentences
    flushTimer = window.setTimeout(flush, 350);
  };
  rec.canceled = (_s, e) => { handlers.onError?.(e.errorDetails || String(e.reason)); };
  rec.sessionStopped = () => { flush(); };

  const scheduleRefresh = () => {
    const ms = Math.max(60, (cfg.expires_in_s || 600) - 60) * 1000;
    refreshTimer = window.setTimeout(async () => {
      try { const t = await api.speechToken(); rec.authorizationToken = t.token; cfg.expires_in_s = t.expires_in_s; scheduleRefresh(); } catch (e: any) { handlers.onError?.(`token refresh failed: ${e?.message || e}`); }
    }, ms);
  };

  return {
    available: true,
    start: () => { startedAt = Date.now(); rec.startContinuousRecognitionAsync(() => { handlers.onStart?.(); scheduleRefresh(); }, (err) => handlers.onError?.(String(err))); },
    stop: () => { if (refreshTimer) window.clearTimeout(refreshTimer); rec.stopContinuousRecognitionAsync(() => { flush(); rec.close(); }, () => rec.close()); },
  };
}

/** Pick the recogniser the deployment configured; Azure needs a token, otherwise the browser's own. */
export async function createRecognizer(cfg: SpeechConfigResponse, handlers: RecognitionHandlers): Promise<Recognizer> {
  if (cfg.stt_provider === "azure" && cfg.token && cfg.region) {
    try {
      return await azureRecognizer(cfg, handlers);
    } catch (e: any) {
      handlers.onError?.(`Azure recognition unavailable (${e?.message || e}); using the browser recogniser`);
    }
  }
  return browserRecognizer(cfg, handlers);
}
