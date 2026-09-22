import { useEffect, useState } from "react";
import { Clinician } from "./clinician/Clinician";
import { Intake } from "./intake/Intake";
import { Status } from "./Status";

function useHash() {
  const [hash, setHash] = useState(window.location.hash);
  useEffect(() => {
    const on = () => setHash(window.location.hash);
    window.addEventListener("hashchange", on);
    return () => window.removeEventListener("hashchange", on);
  }, []);
  return hash;
}

export default function App() {
  const hash = useHash();
  const m = hash.match(/^#\/clinician\/([a-z0-9]+)/i);
  return (
    <div className="app">
      <nav className="top">
        <a href="#/">AI DOC · Dr Sam</a>
        <span className="small">History taking and documentation. No diagnosis, no triage, no advice.</span>
      </nav>
      {m ? <Clinician cid={m[1]} /> : hash.startsWith("#/status") ? <Status /> : <Intake />}
    </div>
  );
}
