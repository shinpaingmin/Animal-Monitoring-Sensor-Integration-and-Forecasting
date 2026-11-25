import { FormEvent, useCallback, useEffect, useState } from "react";

import { ModuleCard } from "./components/ModuleCard";
import { api } from "./services/api";
import type { CaseRecord, HealthStatus } from "./types/contracts";

const modules = [
  { code: "A", title: "Case intake", detail: "Multilingual complaints, triage and duplicate review" },
  { code: "B", title: "Animal detection", detail: "Cat and chicken detections with human verification" },
  { code: "C", title: "Hotspots", detail: "Zone risk, maps, forecasts and early warnings" },
  { code: "D", title: "Actions", detail: "Sourced recommendations and supervisor approval" },
];

function App() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [cases, setCases] = useState<CaseRecord[]>([]);
  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const refresh = useCallback(async () => {
    try {
      const [healthResult, caseResult] = await Promise.all([api.health(), api.listCases()]);
      setHealth(healthResult);
      setCases(caseResult);
    } catch {
      setHealth(null);
      setMessage("The API is unavailable. Start the FastAPI service on port 8000.");
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  async function submitComplaint(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formElement = event.currentTarget;
    const form = new FormData(formElement);
    setSubmitting(true);
    setMessage("");
    try {
      const created = await api.createCase({
        text: String(form.get("text")),
        language: String(form.get("language")),
        block: String(form.get("block")),
        floor: String(form.get("floor")) || null,
        stairwell: String(form.get("stairwell")) || null,
        zone_id: "zone-demo",
        photo_urls: [],
      });
      setCases((current) => [created, ...current]);
      setMessage(`Complaint received. Reference: ${created.id}`);
      formElement.reset();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Unable to submit complaint.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-white/10 bg-slate-950/90">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-emerald-400">Habitat</p>
            <h1 className="text-xl font-semibold">Animal Monitoring System</h1>
          </div>
          <span className={`rounded-full px-3 py-1 text-xs font-medium ${health ? "bg-emerald-400/15 text-emerald-300" : "bg-amber-400/15 text-amber-300"}`}>
            API {health ? "connected" : "offline"}
          </span>
        </div>
      </header>

      <main className="mx-auto max-w-6xl space-y-10 px-6 py-10">
        <section>
          <p className="max-w-2xl text-slate-400">A typed integration baseline for resident reporting, officer review and evidence-led animal management.</p>
          <div className="mt-6 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {modules.map((module) => <ModuleCard key={module.code} {...module} />)}
          </div>
        </section>

        <section className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <h2 className="text-lg font-semibold">Submit a complaint</h2>
            <p className="mt-1 text-sm text-slate-400">No account required in the planned resident workflow.</p>
            <form className="mt-6 grid gap-4" onSubmit={submitComplaint}>
              <label className="grid gap-2 text-sm">What happened?
                <textarea className="field min-h-28" name="text" minLength={5} required placeholder="Describe the animal sighting or welfare concern" />
              </label>
              <div className="grid gap-4 sm:grid-cols-2">
                <label className="grid gap-2 text-sm">Language
                  <select className="field" name="language" defaultValue="en">
                    <option value="en">English</option><option value="zh">Chinese</option><option value="ms">Malay</option><option value="ta">Tamil</option>
                  </select>
                </label>
                <label className="grid gap-2 text-sm">Block
                  <input className="field" name="block" required placeholder="e.g. 101" />
                </label>
                <label className="grid gap-2 text-sm">Floor
                  <input className="field" name="floor" placeholder="e.g. 03" />
                </label>
                <label className="grid gap-2 text-sm">Stairwell
                  <input className="field" name="stairwell" placeholder="e.g. A" />
                </label>
              </div>
              <button className="rounded-lg bg-emerald-400 px-4 py-3 font-semibold text-slate-950 transition hover:bg-emerald-300 disabled:opacity-50" disabled={submitting}>
                {submitting ? "Submitting…" : "Submit complaint"}
              </button>
              {message && <p className="text-sm text-emerald-300" role="status">{message}</p>}
            </form>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold">Recent cases</h2>
              <span className="text-sm text-slate-400">{cases.length} total</span>
            </div>
            <div className="mt-5 space-y-3">
              {cases.length === 0 && <p className="rounded-xl border border-dashed border-white/10 p-6 text-center text-sm text-slate-400">No cases submitted in this session.</p>}
              {cases.map((item) => (
                <article className="rounded-xl bg-slate-900/70 p-4" key={item.id}>
                  <div className="flex justify-between gap-4"><strong className="text-sm text-emerald-300">{item.id}</strong><span className="text-xs uppercase text-slate-500">{item.status}</span></div>
                  <p className="mt-2 line-clamp-2 text-sm text-slate-300">{item.text}</p>
                  <p className="mt-3 text-xs text-slate-500">Block {item.block}{item.floor ? ` · Floor ${item.floor}` : ""}</p>
                </article>
              ))}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
