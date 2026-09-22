import { useEffect, useState } from "react";
import { api } from "./api";

export function Status() {
  const [s, setS] = useState<any>(null);
  useEffect(() => { api.contentStatus().then(setS).catch((e) => setS({ error: String(e) })); }, []);
  return (
    <div className="consent">
      <h1>Content and providers</h1>
      {s ? <pre>{JSON.stringify(s, null, 2)}</pre> : <p>Loading…</p>}
      <p className="small"><a href="#/">Back</a></p>
    </div>
  );
}
