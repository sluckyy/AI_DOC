import { useEffect, useState } from "react";
import { api } from "../api";
import { speakBrowser } from "../drsam/speech";

export function Clinician({ cid }: { cid: string }) {
  const [h, setH] = useState<any>(null);
  const [cd, setCd] = useState<any>(null);
  const [err, setErr] = useState<string | null>(null);
  const [q, setQ] = useState("");
  const [qa, setQa] = useState<{ q: string; a: string }[]>([]);
  const [clinician, setClinician] = useState("");
  const [principal, setPrincipal] = useState("");
  const [additional, setAdditional] = useState("");
  const [attested, setAttested] = useState<any>(null);
  const [tab, setTab] = useState<"handover" | "record" | "coding" | "export">("handover");
  const [exp, setExp] = useState<any>(null);

  useEffect(() => {
    api.handover(cid).then(setH).catch((e) => setErr(String(e.message || e)));
    api.codingDocument(cid).then(setCd).catch(() => {});
  }, [cid]);

  if (err) return <div className="consent"><h1>Handover</h1><p className="error">{err}</p><p>The conversation may still be running.</p></div>;
  if (!h) return <div className="consent"><p>Loading…</p></div>;

  return (
    <div className="clin">
      <header>
        <h1>Handover · {cid}</h1>
        <div className="tabs">
          {(["handover", "record", "coding", "export"] as const).map((t) => (
            <button key={t} className={tab === t ? "on" : ""} onClick={async () => { setTab(t); if (t === "export" && !exp) setExp(await api.exportAll(cid)); }}>{t}</button>
          ))}
        </div>
      </header>
      {h.alerts?.length > 0 && (
        <div className="alerts">
          {h.alerts.map((a: any) => (
            <div key={a.id} className="alertBox">
              <strong>{a.tier.replace("_", " ").toUpperCase()}</strong> · rule {a.rule_id} · routed to {a.route} · {a.fired_at}
              <div>{a.text}</div>
            </div>
          ))}
        </div>
      )}
      {tab === "handover" && (
        <section>
          <button onClick={() => speakBrowser(h.narrative.join(" "), "en-AU", 1.0)}>Hear the handover</button>
          {h.narrative.map((p: string, i: number) => <p key={i} className={p.startsWith("ALERT") ? "alertLine" : p.startsWith("Not asked") ? "notAsked" : ""}>{p}</p>)}
          <h3>Safety-net given to the patient</h3>
          {h.safety_net_record?.uncertainty ? (
            <ul>
              <li>{h.safety_net_record.uncertainty}</li>
              <li>Watch for: {h.safety_net_record.watch_for?.join("; ")}</li>
              <li>{h.safety_net_record.time_course}</li>
              <li>{h.safety_net_record.where}</li>
            </ul>
          ) : <p>None delivered (interview stopped by an alert).</p>}
          <h3>Ask Dr Sam about this history</h3>
          <p className="small">Answers come only from what was asked and recorded. Anything else is "I didn't ask".</p>
          <form onSubmit={async (e) => { e.preventDefault(); const question = q; setQ(""); const r = await api.ask(cid, question); setQa((x) => [...x, { q: question, a: r.answer }]); }}>
            <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="What did they say about…" />
            <button type="submit" disabled={!q.trim()}>Ask</button>
          </form>
          {qa.map((x, i) => <div key={i} className="qa"><div><strong>Q</strong> {x.q}</div><div><strong>Dr Sam</strong> {x.a}</div></div>)}
          <p className="small">Versions: {JSON.stringify(h.versions)}</p>
        </section>
      )}
      {tab === "record" && (
        <section>
          <table>
            <thead><tr><th>Slot</th><th>Class</th><th>Value</th><th>Verbatim</th><th>State</th><th>Turn</th><th>Evidence</th></tr></thead>
            <tbody>
              {h.structured_record.map((e: any) => (
                <tr key={e.slot_id} className={e.state}>
                  <td>{e.slot_id}<div className="small">{e.intent}</div></td><td>{e.class}</td>
                  <td>{e.value === null ? <em>{e.state === "not_asked" ? "not asked" : "unknown"}</em> : Array.isArray(e.value) ? e.value.join(", ") : String(e.value)}</td>
                  <td className="small">{e.verbatim || ""}</td><td>{e.state}</td><td className="small">{e.turn_id || ""}</td><td className="small">{e.evidence || ""}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}
      {tab === "coding" && cd && (
        <section>
          <div className="diagBlock">
            <h3>Diagnosis block · clinician only</h3>
            <p className="small">{cd.coding_document.diagnosis_block.prompt}</p>
            <label>Principal diagnosis <input value={principal} onChange={(e) => setPrincipal(e.target.value)} placeholder="left empty by the agent" /></label>
            <label>Additional diagnoses <input value={additional} onChange={(e) => setAdditional(e.target.value)} placeholder="comma separated" /></label>
          </div>
          <h3>Reason for encounter · patient-reported</h3>
          <p>"{cd.coding_document.reason_for_encounter.patient_words}"</p>
          <p className="small">Concepts: {cd.coding_document.reason_for_encounter.concepts.map((c: any) => `${c.display} [${c.edition} ${c.code}]`).join("; ")}</p>
          <h3>Symptom detail · patient-reported</h3>
          <ul>{cd.coding_document.symptom_detail.items.filter((e: any) => e.state === "filled").map((e: any) => <li key={e.slot_id}>{e.intent}: {Array.isArray(e.value) ? e.value.join(", ") : String(e.value)}</li>)}</ul>
          <h3>Gaps · structural</h3>
          <ul>{cd.coding_document.gaps.items.map((g: string, i: number) => <li key={i}>{g}</li>)}</ul>
          <p className="small">{cd.coding_document.terminology}</p>
          <p className="small">{cd.coding_document.provenance_and_attestation.statement}</p>
          <h3>Attestation</h3>
          <p className="small">An act, not a click: review, edit, fill or leave the diagnosis block, and sign. Only the signed version is exportable.</p>
          {!attested ? (
            <form onSubmit={async (e) => { e.preventDefault(); const r = await api.attest(cid, clinician, { principal_diagnosis: principal || null, additional_diagnoses: additional ? additional.split(",").map((s) => s.trim()) : [] }, {}); setAttested(r); }}>
              <label>Clinician name <input value={clinician} onChange={(e) => setClinician(e.target.value)} required /></label>
              <button type="submit" className="primary" disabled={!clinician.trim()}>I have reviewed this document and sign it</button>
            </form>
          ) : <p className="ok">Attested by {attested.clinician} at {attested.signed_at}. {attested.status}</p>}
        </section>
      )}
      {tab === "export" && (
        <section>
          <h3>Study record</h3>
          {exp ? (
            <>
              <p className="small">Process check (P1 to P14 transcript tests): {exp.process_check.length === 0 ? "no violations" : JSON.stringify(exp.process_check)}</p>
              <pre>{JSON.stringify(exp, null, 2)}</pre>
            </>
          ) : <p>Loading…</p>}
        </section>
      )}
      <p className="small"><a href="#/">New conversation</a></p>
    </div>
  );
}
