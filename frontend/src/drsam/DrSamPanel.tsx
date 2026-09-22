import { useEffect, useRef, useState } from "react";
import { Avatar, Expression } from "./Avatar";
import type { AgentTurn } from "../api";
import { api } from "../api";
import { LANGUAGES } from "../config";
import { makeRecognizer, playAudio, speakBrowser, SpeakHandle } from "./speech";

type Props = {
  cid: string;
  language: string;
  register: string;
  initialTurns: AgentTurn[];
  onEnded: () => void;
};

type Line = { role: "agent" | "person"; text: string; move?: string; alert?: boolean };

export function DrSamPanel({ cid, language, register, initialTurns, onEnded }: Props) {
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
  const [tone, setTone] = useState<string | null>(null);
  const [captionsLarge, setCaptionsLarge] = useState(register === "older");
  const reduced = typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
  const handle = useRef<SpeakHandle | null>(null);
  const queue = useRef<AgentTurn[]>([]);
  const speakingRef = useRef(false);
  const bcp47 = LANGUAGES[language]?.bcp47 || "en-AU";
  const recRef = useRef<ReturnType<typeof makeRecognizer> | null>(null);
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

  async function send(text: string, prosody: Record<string, number> = {}, conf?: number) {
    if (!text.trim() || busy || ended) return;
    setBusy(true);
    setInterim("");
    setLines((l) => [...l, { role: "person", text }]);
    try {
      const r = await api.turn(cid, text, prosody, conf);
      setPhase(r.phase);
      setTone(r.detected_tone?.label || null);
      await playTurns(r.agent_turns);
    } catch (e: any) {
      setLines((l) => [...l, { role: "agent", text: "Sorry, I lost the connection for a moment. Could you say that again?" }]);
    } finally {
      setBusy(false);
    }
  }

  function startListening() {
    if (recRef.current?.available === false) return;
    const rec = makeRecognizer(bcp47, {
      onStart: () => setListening(true),
      onInterim: (t) => {
        setInterim(t);
        // barge-in: the person started talking while Dr Sam speaks; stop unless it is an alert turn
        if (speakingRef.current && !alertMode.current && handle.current) { handle.current.cancel(); queue.current = []; speakingRef.current = false; setSpeaking(false); setViseme(0); }
        setExpression("listening");
      },
      onFinal: (t, conf, dur) => {
        const words = t.split(/\s+/).filter(Boolean).length;
        const wpm = dur > 0 ? Math.round((words / dur) * 60000) : 0;
        send(t, { words_per_minute: wpm, duration_ms: dur, word_count: words }, conf);
      },
      onError: (e) => { if (e === "not-allowed" || e === "service-not-allowed") { setMicAvailable(false); setListening(false); } },
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
        <div className="meta">phase: {phase}{tone && tone !== "settled" ? ` · pace adapted (${tone})` : ""}</div>
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
        {ended && <div className="endedNote">This conversation has ended. Everything you said, in your own words, goes to the doctor.</div>}
      </div>
    </div>
  );
}
