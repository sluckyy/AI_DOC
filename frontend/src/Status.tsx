import { useEffect, useState } from "react";
import { api } from "./api";

/** Content and provider status: what will run, what is reviewed, what the owner still has to set. */
export function Status() {
  const [s, setS] = useState<any>(null);
  useEffect(() => { api.contentStatus().then(setS).catch((e) => setS({ error: String(e) })); }, []);
  if (!s) return <div className="consent"><h1>Content and providers</h1><p>Loading…</p></div>;
  if (s.error) return <div className="consent"><h1>Content and providers</h1><p className="error">{s.error}</p></div>;
  const modules: any[] = s.modules || [];
  const reviewed = modules.filter((m) => m.reviewed).length;
  const disabled = Object.entries(s.disabled_modules || {});
  const pending = Object.entries(s.clinical_parameters || {}).filter(([, v]: any) => v.status !== "set");
  return (
    <div className="consent">
      <h1>Content and providers</h1>
      <p className="small">
        {modules.length} modules live, {reviewed} reviewed for simulation. Content {s.content_version} ({s.content_mode} mode); parameters {s.parameters}; context v{s.context_version}.
        Authoring checks {s.authoring_checks?.passed ? "passed" : "FAILED"}. Telephony: {s.telephony}.
      </p>
      {disabled.length > 0 && (
        <p className="small">Present but not live (D-52): {disabled.map(([k, v]) => `${k} v${v}`).join(", ")}.</p>
      )}
      {pending.length > 0 && (
        <p className="small">Owner-set clinical parameters still pending (see design/09): {pending.map(([k]) => k).join(", ")}.</p>
      )}
      <table className="status-table">
        <thead><tr><th>Module</th><th>Version</th><th>Review status</th><th>Slots</th><th>Red flags</th><th>Open review notes</th></tr></thead>
        <tbody>
          {modules.map((m) => (
            <tr key={m.module}>
              <td>{m.display_name}</td>
              <td>{m.version}</td>
              <td>{m.review_status}{m.reviewed ? ` (${m.reviewed_by || ""} ${m.reviewed_on || ""})` : ""}</td>
              <td>{m.slots}</td>
              <td>{(m.red_flags || []).map((r: any) => `${r.id} [${r.tier}]`).join(", ")}</td>
              <td>{(m.review_notes || []).join("; ")}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <details><summary>Raw status</summary><pre>{JSON.stringify(s, null, 2)}</pre></details>
      <p className="small"><a href="#/">Back</a></p>
    </div>
  );
}
