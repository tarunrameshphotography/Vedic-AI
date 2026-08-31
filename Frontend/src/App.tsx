import { useState } from "react";
import { consult } from "./api";
import { ApiError, DEFAULT_BIRTH_INPUT, type BirthInput, type ConsultResult } from "./types";
import { AdjudicationView } from "./components/AdjudicationView";
import { BirthForm } from "./components/BirthForm";
import { CaseManager } from "./components/CaseManager";
import { ChartView } from "./components/ChartView";
import { ClaimsExplorer } from "./components/ClaimsExplorer";
import { ComparisonMode } from "./components/ComparisonMode";
import { ConsultationSummary } from "./components/ConsultationSummary";
import { DasaTimeline } from "./components/DasaTimeline";
import { DeferredView } from "./components/DeferredView";
import { FactInspector } from "./components/FactInspector";
import { VerificationView } from "./components/VerificationView";

const TABS = [
  "Run Consultation",
  "Claims",
  "Dasa Timeline",
  "Adjudications",
  "Deferred",
  "Facts",
  "Verification",
  "Chart",
  "Compare",
  "Saved Charts",
] as const;
type Tab = (typeof TABS)[number];

export default function App() {
  const [birth, setBirth] = useState<BirthInput>(DEFAULT_BIRTH_INPUT);
  const [result, setResult] = useState<ConsultResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [tab, setTab] = useState<Tab>("Run Consultation");

  async function handleSubmit(value: BirthInput) {
    setLoading(true);
    setError(null);
    try {
      const r = await consult(value);
      setResult(r);
      // Stay on "Run Consultation": §7 requires the chart summary to be
      // shown right after a successful run, and that summary only renders
      // on this tab. The user picks Claims/Dasa/etc. themselves from here.
    } catch (e) {
      setError(e instanceof ApiError ? e.message : String(e));
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  const needsResult: Tab[] = ["Claims", "Dasa Timeline", "Adjudications", "Facts", "Verification", "Chart"];

  return (
    <div className="app-shell">
      <header>
        <h1>VEDIC-AI Consultation Inspector</h1>
        <p className="muted">
          A developer testing interface over the existing astrology reasoning engine. This
          UI computes nothing itself and invents no explanation beyond what the engine
          already produced.
        </p>
      </header>

      <nav className="tabs" aria-label="Views">
        {TABS.map((t) => (
          <button
            key={t}
            type="button"
            className={t === tab ? "active" : ""}
            onClick={() => setTab(t)}
            disabled={needsResult.includes(t) && !result}
            aria-current={t === tab ? "page" : undefined}
          >
            {t}
          </button>
        ))}
      </nav>

      <main>
        {tab === "Run Consultation" && (
          <section>
            <h2>Birth Data</h2>
            <BirthForm value={birth} onChange={setBirth} onSubmit={handleSubmit} submitting={loading} />
            {error && (
              <p className="fail" role="alert">
                {error}
              </p>
            )}
            {result && <ConsultationSummary result={result} />}
          </section>
        )}

        {tab === "Claims" && result && (
          <ClaimsExplorer claims={result.claims} verification={result.verification} />
        )}

        {tab === "Dasa Timeline" && result && (
          <DasaTimeline timeline={result.dasa_timeline} claims={result.claims} />
        )}

        {tab === "Adjudications" && result && (
          <AdjudicationView adjudications={result.adjudications} />
        )}

        {tab === "Deferred" && result && <DeferredView coverage={result.coverage} />}
        {tab === "Deferred" && !result && (
          <DeferredView
            coverage={{
              cards_in_store: 0,
              candidates_from_index: 0,
              claims_activated: 0,
              inert_cards: [],
              out_of_scope: [],
              reference_cards: [],
              not_covered: [],
              loaded_doctrine: [],
            }}
          />
        )}

        {tab === "Facts" && result && <FactInspector facts={result.facts} />}
        {tab === "Verification" && result && <VerificationView verification={result.verification} />}
        {tab === "Chart" && result && <ChartView chart={result.chart} />}
        {tab === "Compare" && <ComparisonMode />}
        {tab === "Saved Charts" && (
          <CaseManager currentBirth={birth} onLoad={(b) => { setBirth(b); setTab("Run Consultation"); }} />
        )}
      </main>
    </div>
  );
}
