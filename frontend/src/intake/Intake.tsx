import { useState } from "react";
import { api, AgentTurn } from "../api";
import { LANGUAGES } from "../config";
import { DrSamPanel } from "../drsam/DrSamPanel";

export function Intake() {
  const [setting, setSetting] = useState<"ed" | "gp_booking">("ed");
  const [language, setLanguage] = useState("en");
  const [register, setRegister] = useState("patient");
  const [ai, setAi] = useState(false);
  const [tone, setTone] = useState(false);
  const [share, setShare] = useState(true);
  const [cid, setCid] = useState<string | null>(null);
  const [turns, setTurns] = useState<AgentTurn[]>([]);
  const [err, setErr] = useState<string | null>(null);
  const [ended, setEnded] = useState(false);

  async function start() {
    setErr(null);
    try {
      const r = await api.start(setting, language, { ai_disclosure: ai, tone_adaptation: tone, summary_to_clinician: share }, register);
      setCid(r.conversation_id);
      setTurns(r.agent_turns);
    } catch (e: any) {
      setErr(String(e.message || e));
    }
  }

  if (cid) {
    return (
      <div>
        <DrSamPanel cid={cid} setting={setting} language={language} register={register} initialTurns={turns} onEnded={() => setEnded(true)} />
        {ended && (
          <p className="afterEnd">
            For the clinician: <a href={`#/clinician/${cid}`}>open the handover for {cid}</a>
          </p>
        )}
      </div>
    );
  }

  return (
    <div className="consent">
      <h1>Before we start</h1>
      <p>
        Dr Sam is an AI, not a doctor. Dr Sam takes your history in your own words and passes it to the clinician looking after you.
        Dr Sam does not diagnose, does not decide how urgent your problem is, and does not give treatment advice. You can stop at any
        time and ask for a person, and you will get the same care either way.
      </p>
      <div className="grid">
        <label>Setting
          <select value={setting} onChange={(e) => setSetting(e.target.value as any)}>
            <option value="ed">Emergency department waiting room</option>
            <option value="gp_booking">GP booking call</option>
          </select>
        </label>
        <label>Language
          <select value={language} onChange={(e) => setLanguage(e.target.value)}>
            {Object.entries(LANGUAGES).map(([k, v]) => <option key={k} value={k}>{v.name}</option>)}
          </select>
        </label>
        <label>Pace
          <select value={register} onChange={(e) => setRegister(e.target.value)}>
            <option value="patient">Standard</option>
            <option value="older">Slower, larger captions</option>
          </select>
        </label>
      </div>
      <div className="switches">
        <label><input type="checkbox" checked={ai} onChange={(e) => setAi(e.target.checked)} /> I understand Dr Sam is an AI and I can ask for a person at any time.</label>
        <label><input type="checkbox" checked={share} onChange={(e) => setShare(e.target.checked)} /> What I say may be passed to the clinician looking after me.</label>
        <label><input type="checkbox" checked={tone} onChange={(e) => setTone(e.target.checked)} /> Dr Sam may adjust its pace to how I seem. (Optional. Nothing about how I seem is used clinically.)</label>
      </div>
      {language !== "en" && <p className="hint">Questions are authored in English for this slice; with the Azure OpenAI provider configured they are spoken in {LANGUAGES[language].name}. The handover is always in English.</p>}
      <button className="primary" onClick={start} disabled={!ai || !share}>Start with Dr Sam</button>
      {err && <p className="error">{err}</p>}
      <p className="small"><a href="#/status">Content and provider status</a></p>
    </div>
  );
}
