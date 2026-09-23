import { useEffect, useRef, useState } from "react";
import { Avatar, Expression } from "./Avatar";
import type { AgentTurn } from "../api";
import { api } from "../api";
import { LANGUAGES } from "../config";
import { playAudio, speakBrowser, SpeakHandle, Recognizer } from "./speech";
import { createRecognizer } from "./recognition";
import { LiveTransfer } from "./LiveTransfer";

type Props = {
  cid: string;
  setting: "ed" | "gp_booking";
  language: string;
  register: string;
  initialTurns: AgentTurn[];
  /** Opened on the Start tap; null when declined or absent (typing only). */
  micStream: MediaStream | null;
  micNote: string | null;
  onEnded: () => void;
};

type Line = { role: "agent" | "person"; text: string; move?: string; alert?: boolean };
type Ear = "starting" | "listening" | "paused" | "unavailable";

const WORD = /[^\p{L}\p{N}']+/u;
function words(t: string) { return t.toLowerCase().split(WORD).filter(Boolean); }

/**
 * Echo guard for ambient listening: with speakers rather than headphones the microphone hears
 * Dr Sam too. Heard text that mostly repeats what Dr Sam is saying (or just said) is echo, not
 * the person, and is dropped rather than sent as a turn. Short genuine answers ("yes", "no",
 * "it hurts") share few words with a question and pass through.
 */
function looksLikeEcho(heard: string, spoken: string[]) {
  const h = words(heard);
  if (h.length < 2) return false;
  const bag = new Set(spoken.flatMap(words));
  if (!bag.size) return false;
  const hits = h.filter((w) => bag.has(w)).length;
  return hits / h.length >= 0.6;
}

export function DrSamPanel({ cid, setting, language, register, initialTurns, micStream, micNote, onEnded }: Props) {
  const [transfer, setTransfer] = useState(false);
  const [expression, setExpression] = useState<Expression>("warm");
  const [viseme, setViseme] = useState(0);
  const [speaking, setSpeaking] = useState(false);
  const [lines, setLines] = useState<Line[]>([]);
  const [interim, setInterim] = useState("");
  const [typed, setTyped] = useState("");
  const [busy, setBusy] = useState(false);
  const [ear, setEar] = useState<Ear>(micStream ? "starting" : "unavailable");
  const [ended, setEnded] = useState(false);
  const [phase, setPhase] = useState("consent");
  const [lang, setLang] = useState(language);
  const [sttNote, setSttNote] = useState<string | null>(micNote);
  const [sttProvider, setSttProvider] = useState<string>("browser");
  const [tone, setTone] = useState<string | null>(null);
  const [captionsLarge, setCaptionsLarge] = useState(register === "older");
  const reduced = typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
  const handle = useRef<SpeakHandle | null>(null);
  const queue = useRef<AgentTurn[]>([]);
  const speakingRef = useRef(false);
  const bcp47 = LANGUAGES[lang]?.bcp47 || "en-AU";
  const recRef = useRef<Recognizer | null>(null);
  const langRef = useRef(language);
  const alertMode = useRef(false);
  // state the recogniser's handlers must see live (they are created once, so React state would be stale)
  const busyRef = useRef(false);
  const endedRef = useRef(false);
  const pausedRef = useRef(false);
  const pending = useRef<{ text: string; asr: Record<string, unknown> | null; prosody: Record<string, number> }[]>([]);
  const recentCaptions = useRef<string[]>([]);
  const lastSpokeAt = useRef(0);
  const restartToken = useRef(0);

  async function playTurns(turns: AgentTurn[]) {
    queue.current.push(...turns);
    if (speakingRef.current) return;
    speakingRef.current = true;
    while (queue.current.length) {
      const t = queue.current.shift()!;
      setLines((l) => [...l, { role: "agent", text: t.caption, move: t.move, alert: t.move === "alert" }]);
      recentCaptions.current = [...recentCaptions.current.slice(-2), t.caption];
      setExpression((t.expression as Expression) || "attentive");
      setSpeaking(true);
      alertMode.current = t.move === "alert";
      // schedule visemes against wall clock
      const start = performance.now();
      const vis = t.visemes || [];
      let i = 0;
      const tick = () => {
        if (!speakingRef.current) return;
        const el = performance.now() - start;
        while (i < vis.length && vis[i].offset_ms <= el) { setViseme(vis[i].viseme_id); i++; }
        if (i < vis.length) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      handle.current = t.audio_url ? playAudio(api.audioUrl(t.audio_url)) : speakBrowser(t.caption, bcp47, register === "older" ? 0.82 : 0.92);
      await handle.current.done;
      lastSpokeAt.current = Date.now();
      setViseme(0);
      setSpeaking(false);
      alertMode.current = false;
      if (t.next === "end") { endedRef.current = true; setEnded(true); stopListening(); onEnded(); }
      await new Promise((r) => setTimeout(r, Math.min(t.prosody?.pause_after_ms || 400, 1500)));
    }
    speakingRef.current = false;
    setExpression((e) => (e === "serious" ? "serious" : "attentive"));
  }

  useEffect(() => { playTurns(initialTurns); /* eslint-disable-next-line */ }, []);

  /** Dr Sam is speaking, or finished within the echo tail the microphone may still deliver. */
  function inEchoWindow() { return speakingRef.current || Date.now() - lastSpokeAt.current < 1500; }

  async function send(text: string, prosody: Record<string, number> = {}, asr?: Record<string, unknown> | null) {
    if (!text.trim() || endedRef.current) return;
    if (busyRef.current) {
      // the person kept talking while the last turn was in flight: keep it, send it next
      pending.current.push({ text, asr: asr || null, prosody });
      return;
    }
    busyRef.current = true;
    setBusy(true);
    setInterim("");
    setLines((l) => [...l, { role: "person", text }]);
    try {
      const r = await api.turn(cid, text, prosody, asr || { provider: "typed", confidence: null });
      setPhase(r.phase);
      if (r.language_switched && r.language !== langRef.current) {
        // the capability check switched the interview language: the recogniser restarts in the new one
        langRef.current = r.language;
        setLang(r.language);
        restartListening();
      }
      setTone(r.detected_tone?.label || null);
      if (setting === "gp_booking" && r.alerts?.some((a: any) => a.tier === "immediate" && a.route === "live_transfer")) setTransfer(true);
      await playTurns(r.agent_turns);
    } catch (e: any) {
      setLines((l) => [...l, { role: "agent", text: "Sorry, I lost the connection for a moment. Could you say that again?" }]);
    } finally {
      busyRef.current = false;
      setBusy(false);
    }
    const next = pending.current;
    if (next.length && !endedRef.current) {
      pending.current = [];
      const joined = next.map((n) => n.text).join(" ");
      const first = next[0];
      void send(joined, first.prosody, first.asr);
    }
  }

  async function startListening() {
    if (!micStream) return;
    const token = ++restartToken.current;
    let cfg;
    try {
      cfg = await api.speechConfig(langRef.current, register);
    } catch {
      cfg = { stt_provider: "browser" as const, region: null, bcp47, silence_end_of_turn_ms: 1200, initial_silence_timeout_ms: 8000, low_confidence_threshold: 0.6, token: null, expires_in_s: null, languages: {}, note: "speech config unavailable; using the browser recogniser" };
    }
    if (token !== restartToken.current) return; // superseded by a later restart
    setSttProvider(cfg.stt_provider);
    setSttNote(cfg.note || null);
    const rec = await createRecognizer(cfg, {
      onStart: () => setEar(pausedRef.current ? "paused" : "listening"),
      onInterim: (t) => {
        if (pausedRef.current || endedRef.current) return;
        if (inEchoWindow() && looksLikeEcho(t, recentCaptions.current)) return;
        setInterim(t);
        // barge-in (N-1): the person started talking while Dr Sam speaks; stop unless it is an alert turn.
        // A couple of words are needed first so a cough or a stray syllable does not cut Dr Sam off.
        if (speakingRef.current && !alertMode.current && handle.current && words(t).length >= 2) {
          handle.current.cancel(); queue.current = []; speakingRef.current = false; setSpeaking(false); setViseme(0);
        }
        setExpression("listening");
      },
      onFinal: (t, asr, prosody) => {
        if (pausedRef.current || endedRef.current) return;
        if (inEchoWindow() && looksLikeEcho(t, recentCaptions.current)) { setInterim(""); return; }
        send(t, prosody, asr);
      },
      onError: (e) => {
        if (e === "not-allowed" || e === "service-not-allowed") { setEar("unavailable"); setSttNote("Microphone access was declined, so you can type your replies instead."); return; }
        setSttNote(e);
      },
    }, micStream);
    if (token !== restartToken.current) { rec.stop(); return; }
    if (!rec.available) { setEar("unavailable"); setSttNote("This browser cannot listen, so you can type your replies instead."); return; }
    recRef.current = rec;
    rec.start();
  }
  function stopListening() { recRef.current?.stop(); recRef.current = null; }
  function restartListening() { stopListening(); setEar("starting"); void startListening(); }
  function togglePause() {
    const paused = !pausedRef.current;
    pausedRef.current = paused;
    micStream?.getAudioTracks().forEach((tr) => { tr.enabled = !paused; });
    setInterim("");
    setEar(paused ? "paused" : "listening");
  }

  // ambient listening: start with the conversation, stop when it ends or the panel unmounts
  useEffect(() => {
    void startListening();
    return () => { restartToken.current++; recRef.current?.stop(); handle.current?.cancel(); micStream?.getTracks().forEach((tr) => tr.stop()); };
    /* eslint-disable-next-line */
  }, []);
  useEffect(() => { if (ended) micStream?.getTracks().forEach((tr) => tr.stop()); }, [ended, micStream]);

  const earLabel =
    ear === "unavailable" ? "Not listening. Type below." :
    ear === "paused" ? "Paused" :
    ear === "starting" ? "Getting ready to listen…" :
    speaking ? "Dr Sam is speaking. You can talk over them." :
    busy ? "Thinking…" : "Listening";

  return (
    <div className="panel">
      <div className="avatarCol">
        <Avatar expression={expression} viseme={viseme} speaking={speaking} reducedMotion={reduced} />
        <div className="badge">Dr Sam · AI, not a doctor</div>
        <div className="meta">phase: {phase}{tone && tone !== "settled" ? ` · pace adapted (${tone})` : ""} · hearing via {sttProvider === "azure" ? "Azure Speech" : "browser"} · {LANGUAGES[lang]?.name || lang}</div>
        {sttNote && <div className="meta small">{sttNote}</div>}
      </div>
      <div className="convoCol">
        <div className={`captions ${captionsLarge ? "large" : ""}`} aria-live="polite">
          {lines.map((l, i) => (
            <div key={i} className={`line ${l.role} ${l.alert ? "alert" : ""}`}>
              <span className="who">{l.role === "agent" ? "Dr Sam" : "You"}</span>
              <span>{l.text}</span>
            </div>
          ))}
          {interim && <div className="line person interim"><span className="who">You</span><span>{interim}…</span></div>}
        </div>
        {!ended && (
          <div className="controls">
            <div className={`ear ${ear}`} role="status" aria-live="polite">
              <span className="dot" aria-hidden="true" />
              <span>{earLabel}</span>
            </div>
            {ear !== "unavailable" && ear !== "starting" && (
              <button type="button" className={ear === "paused" ? "mic" : "mic on"} onClick={togglePause}>
                {ear === "paused" ? "Resume listening" : "Pause listening"}
              </button>
            )}
            <form onSubmit={(e) => { e.preventDefault(); const t = typed; setTyped(""); send(t); }} className="typeRow">
              <input value={typed} onChange={(e) => setTyped(e.target.value)} placeholder="Or type here" aria-label="Type your reply" />
              <button type="submit" disabled={!typed.trim()}>Send</button>
            </form>
            <label className="small"><input type="checkbox" checked={captionsLarge} onChange={(e) => setCaptionsLarge(e.target.checked)} /> Large captions</label>
          </div>
        )}
        {transfer && <LiveTransfer cid={cid} />}
        {ended && <div className="endedNote">This conversation has ended. Everything you said, in your own words, goes to the doctor.</div>}
      </div>
    </div>
  );
}
