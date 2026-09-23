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
  onEnded: () => void;
};

type Line = { role: "agent" | "person"; text: string; move?: string; alert?: boolean };

export function DrSamPanel({ cid, setting, language, register, initialTurns, onEnded }: Props) {
  const [transfer, setTransfer] = useState(false);
  const [expression, setExpression] = useState<Expression>("warm");
  const [viseme, setViseme] = useState(0);
  const [speaking, setSpeaking] = useState(false);
  const [lines, setLines] = useState<Line[]>([]);
  const [interim, setInterim] = useState("");
  const [typed, setTyped] = useState("");
  const [busy, setBusy] = useState(false);
  const [listening, setListening] = useState(false);
  const [micAvailable, setMicAvailable] = useState(true);
  const [ended, setEnded] = useState(false);
  const [phase, setPhase] = useState("consent");
  const [lang, setLang] = useState(language);
  const [sttNote, setSttNote] = useState<string | null>(null);
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

  async function playTurns(turns: AgentTurn[]) {
    queue.current.push(...turns);
    if (speakingRef.current) return;
    speakingRef.current = true;
    while (queue.current.length) {
      const t = queue.current.shift()!;
      setLines((l) => [...l, { role: "agent", text: t.caption, move: t.move, alert: t.move === "alert" }]);
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
      setViseme(0);
      setSpeaking(false);
      alertMode.current = false;
      if (t.next === "end") { setEnded(true); onEnded(); }
      await new Promise((r) => setTimeout(r, Math.min(t.prosody?.pause_after_ms || 400, 1500)));
    }
    speakingRef.current = false;
    setExpression((e) => (e === "serious" ? "serious" : "attentive"));
  }

  useEffect(() => { playTurns(initialTurns); /* eslint-disable-next-line */ }, []);

  async function send(text: string, prosody: Record<string, number> = {}, asr?: Record<string, unknown> | null) {
    if (!text.trim() || busy || ended) return;
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
        if (recRef.current) { recRef.current.stop(); recRef.current = null; setListening(false); }
      }
      setTone(r.detected_tone?.label || null);
      if (setting === "gp_booking" && r.alerts?.some((a: any) => a.tier === "immediate" && a.route === "live_transfer")) setTransfer(true);
      await playTurns(r.agent_turns);
    } catch (e: any) {
      setLines((l) => [...l, { role: "agent", text: "Sorry, I lost the connection for a moment. Could you say that again?" }]);
    } finally {
      setBusy(false);
    }
  }

  async function startListening() {
    if (recRef.current?.available === false) return;
    let cfg;
    try {
      cfg = await api.speechConfig(langRef.current, register);
    } catch {
      cfg = { stt_provider: "browser" as const, region: null, bcp47, silence_end_of_turn_ms: 1200, initial_silence_timeout_ms: 8000, low_confidence_threshold: 0.6, token: null, expires_in_s: null, languages: {}, note: "speech config unavailable; using the browser recogniser" };
    }
    setSttProvider(cfg.stt_provider);
    setSttNote(cfg.note || null);
    const rec = await createRecognizer(cfg, {
      onStart: () => setListening(true),
      onInterim: (t) => {
        setInterim(t);
        // barge-in (N-1): the person started talking while Dr Sam speaks; stop unless it is an alert turn
        if (speakingRef.current && !alertMode.current && handle.current) { handle.current.cancel(); queue.current = []; speakingRef.current = false; setSpeaking(false); setViseme(0); }
        setExpression("listening");
      },
      onFinal: (t, asr, prosody) => send(t, prosody, asr),
      onError: (e) => {
        if (e === "not-allowed" || e === "service-not-allowed") { setMicAvailable(false); setListening(false); return; }
        setSttNote(e);
      },
    });
    if (!rec.available) { setMicAvailable(false); return; }
    recRef.current = rec;
    rec.start();
  }
  function stopListening() { recRef.current?.stop(); setListening(false); }

  useEffect(() => () => { recRef.current?.stop(); handle.current?.cancel(); }, []);

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
            {micAvailable ? (
              <button className={listening ? "mic on" : "mic"} onClick={listening ? stopListening : startListening} disabled={busy}>
                {listening ? "Listening… tap to stop" : "Tap to talk"}
              </button>
            ) : (
              <span className="hint">Microphone unavailable in this browser. Type instead.</span>
            )}
            <form onSubmit={(e) => { e.preventDefault(); const t = typed; setTyped(""); send(t); }} className="typeRow">
              <input value={typed} onChange={(e) => setTyped(e.target.value)} placeholder="Or type here" aria-label="Type your reply" disabled={busy} />
              <button type="submit" disabled={busy || !typed.trim()}>Send</button>
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
