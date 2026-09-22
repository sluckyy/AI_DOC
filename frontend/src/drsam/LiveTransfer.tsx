/**
 * D-42: the GP booking call's Immediate tier transfers the call live to the duty GP.
 * For the demo the number is configured on the server (DEMO_TRANSFER_NUMBER). With the
 * Azure Communication Services provider the browser dials the number over PSTN; in fake
 * mode it shows the number, offers a tel: link, and lets the receiving GP acknowledge.
 */
import { useEffect, useState } from "react";
import { API_BASE } from "../config";

type Setup = {
  route: string; transfer_target: string | null; unanswered: string | null; provider: string;
  transfer_number: string | null; caller_id: string | null; token: string | null; user_id: string | null;
  alert: { alert_id: string; text: string; verbatim: string | null; fired_at: string; rule_id: string; tier: string };
};

export function LiveTransfer({ cid }: { cid: string }) {
  const [setup, setSetup] = useState<Setup | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [status, setStatus] = useState<"preparing" | "ringing" | "connected" | "acknowledged" | "failed">("preparing");
  const [ackBy, setAckBy] = useState("");
  const [callState, setCallState] = useState<string>("");

  useEffect(() => {
    fetch(`${API_BASE}/conversations/${cid}/transfer`, { method: "POST" })
      .then(async (r) => { if (!r.ok) throw new Error(await r.text()); return r.json(); })
      .then((s: Setup) => { setSetup(s); setStatus("ringing"); if (s.token && s.transfer_number) startAcsCall(s); })
      .catch((e) => { setErr(String(e.message || e)); setStatus("failed"); });
    // eslint-disable-next-line
  }, [cid]);

  async function startAcsCall(s: Setup) {
    try {
      // Loaded on demand so the demo bundle does not require the SDK to be present.
      const callingModule = "@azure/communication-calling";
      const commonModule = "@azure/communication-common";
      const calling: any = await import(/* @vite-ignore */ callingModule);
      const common: any = await import(/* @vite-ignore */ commonModule);
      const credential = new common.AzureCommunicationTokenCredential(s.token);
      const client = new calling.CallClient();
      const agent = await client.createCallAgent(credential);
      const dm = await client.getDeviceManager();
      await dm.askDevicePermission({ audio: true, video: false });
      const call = agent.startCall([{ phoneNumber: s.transfer_number }], s.caller_id ? { alternateCallerId: { phoneNumber: s.caller_id } } : {});
      call.on("stateChanged", () => { setCallState(call.state); if (call.state === "Connected") setStatus("connected"); if (call.state === "Disconnected") setStatus((st) => (st === "acknowledged" ? st : "failed")); });
    } catch (e: any) {
      setCallState(`ACS unavailable (${e?.message || e}); showing the number instead`);
    }
  }

  async function acknowledge() {
    if (!setup) return;
    const r = await fetch(`${API_BASE}/alerts/${setup.alert.alert_id}/acknowledge`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ acknowledged_by: ackBy }) });
    if (r.ok) setStatus("acknowledged");
  }

  return (
    <div className="transfer">
      <h3>Transferring to the duty doctor</h3>
      {err && <p className="error">{err}</p>}
      {setup && (
        <>
          <p className="small">Route: {setup.route} · target: {setup.transfer_target} · if unanswered: {setup.unanswered} · provider: {setup.provider}</p>
          <div className="alertBox">
            <strong>{setup.alert.tier.toUpperCase()}</strong> · rule {setup.alert.rule_id} · {setup.alert.fired_at}
            <div>{setup.alert.text}</div>
          </div>
          {status === "ringing" && setup.transfer_number && (
            <p>Calling <a href={`tel:${setup.transfer_number}`}>{setup.transfer_number}</a>{callState ? ` · ${callState}` : " · ringing…"}</p>
          )}
          {status === "ringing" && !setup.transfer_number && <p className="error">No transfer number is configured (DEMO_TRANSFER_NUMBER). The alert stands and is recorded; the practice's own workflow applies.</p>}
          {status === "connected" && <p className="ok">Connected. The patient is speaking with the duty doctor.</p>}
          {status !== "acknowledged" ? (
            <form onSubmit={(e) => { e.preventDefault(); acknowledge(); }} className="typeRow">
              <input value={ackBy} onChange={(e) => setAckBy(e.target.value)} placeholder="Receiving clinician's name" aria-label="Receiving clinician" />
              <button type="submit" disabled={!ackBy.trim()}>Acknowledge alert</button>
            </form>
          ) : <p className="ok">Alert acknowledged by {ackBy}. Recorded with a timestamp.</p>}
          <p className="small">Every alert requires positive acknowledgement by a named person (S-4). Unacknowledged alerts appear on the duty list for further escalation.</p>
        </>
      )}
    </div>
  );
}
