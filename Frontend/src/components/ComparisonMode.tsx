import { useState } from "react";
import { consult } from "../api";
import { ApiError, DEFAULT_BIRTH_INPUT, type BirthInput, type Claim, type ConsultResult } from "../types";
import { BirthForm } from "./BirthForm";

function setDiff(as: string[], bs: string[]) {
  const A = new Set(as);
  const B = new Set(bs);
  return {
    onlyA: [...new Set(as)].filter((x) => !B.has(x)).sort(),
    onlyB: [...new Set(bs)].filter((x) => !A.has(x)).sort(),
    shared: [...new Set(as)].filter((x) => B.has(x)).sort(),
  };
}

// `claim_id` (clm-0001…) is a per-run sequential index, not a stable
// identity across two different birth charts -- comparing raw ids would be
// meaningless noise. A claim's real identity across charts is which rule
// card fired and, for a quantified card, which variables it bound (which
// graha satisfied it) -- so that pair is the comparison key, not the id.
export function claimSignature(c: Claim): string {
  const vars = Object.entries(c.derived.variables)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([k, v]) => `${k}=${v}`)
    .join(",");
  return vars ? `${c.derived.rule_card}[${vars}]` : c.derived.rule_card;
}

export interface ComparisonDiff {
  claims: ReturnType<typeof setDiff>; // by (rule_card, variables) signature
  ruleCards: ReturnType<typeof setDiff>; // by rule_card alone
  facts: ReturnType<typeof setDiff>; // by fact key
  contradictions: ReturnType<typeof setDiff>; // by "subject|relationship"
  deferredOnThisChart: ReturnType<typeof setDiff>; // inert_cards + reference_cards lines
  dasaOrdinalDifferences: Array<{ graha: string; ordinalA: number; ordinalB: number }>;
}

/** A structural comparison only (§16). Never ranks or declares one chart
 * "better" or "more accurate" -- every field here is a set operation over
 * data both consultations already produced. */
export function diffConsultations(a: ConsultResult, b: ConsultResult): ComparisonDiff {
  const claims = setDiff(a.claims.map(claimSignature), b.claims.map(claimSignature));
  const ruleCards = setDiff(
    a.claims.map((c) => c.derived.rule_card),
    b.claims.map((c) => c.derived.rule_card),
  );
  const facts = setDiff(
    a.facts.items.map((f) => f.key),
    b.facts.items.map((f) => f.key),
  );
  const contradictions = setDiff(
    a.adjudications.map((adj) => `${adj.subject}|${adj.relationship}`),
    b.adjudications.map((adj) => `${adj.subject}|${adj.relationship}`),
  );
  const deferredOnThisChart = setDiff(
    [...a.coverage.inert_cards, ...a.coverage.reference_cards],
    [...b.coverage.inert_cards, ...b.coverage.reference_cards],
  );

  const byGrahaA = new Map(a.dasa_timeline.map((p) => [p.graha, p.ordinal]));
  const dasaOrdinalDifferences = b.dasa_timeline
    .filter((p) => byGrahaA.has(p.graha) && byGrahaA.get(p.graha) !== p.ordinal)
    .map((p) => ({ graha: p.graha, ordinalA: byGrahaA.get(p.graha)!, ordinalB: p.ordinal }));

  return { claims, ruleCards, facts, contradictions, deferredOnThisChart, dasaOrdinalDifferences };
}

function DiffList({ title, diff }: { title: string; diff: ReturnType<typeof setDiff> }) {
  return (
    <details>
      <summary>
        {title} — {diff.shared.length} shared, {diff.onlyA.length} only in A,{" "}
        {diff.onlyB.length} only in B
      </summary>
      <div className="diff-columns">
        <div>
          <h4>Only in A ({diff.onlyA.length})</h4>
          <ul>{diff.onlyA.map((x) => <li key={x}><code>{x}</code></li>)}</ul>
        </div>
        <div>
          <h4>Only in B ({diff.onlyB.length})</h4>
          <ul>{diff.onlyB.map((x) => <li key={x}><code>{x}</code></li>)}</ul>
        </div>
        <div>
          <h4>Shared ({diff.shared.length})</h4>
          <ul>{diff.shared.map((x) => <li key={x}><code>{x}</code></li>)}</ul>
        </div>
      </div>
    </details>
  );
}

export function ComparisonMode() {
  const [birthA, setBirthA] = useState<BirthInput>(DEFAULT_BIRTH_INPUT);
  const [birthB, setBirthB] = useState<BirthInput>(DEFAULT_BIRTH_INPUT);
  const [resultA, setResultA] = useState<ConsultResult | null>(null);
  const [resultB, setResultB] = useState<ConsultResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function runBoth() {
    setError(null);
    setLoading(true);
    try {
      const [a, b] = await Promise.all([consult(birthA), consult(birthB)]);
      setResultA(a);
      setResultB(b);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  }

  const diff = resultA && resultB ? diffConsultations(resultA, resultB) : null;

  return (
    <section>
      <h2>Compare Two Charts</h2>
      <p className="muted">
        A structural comparison only -- this never says one chart is "better" or "more
        accurate" than the other.
      </p>
      <div className="compare-columns">
        <div>
          <h3>Chart A</h3>
          <BirthForm value={birthA} onChange={setBirthA} onSubmit={() => undefined} submitting={false} />
        </div>
        <div>
          <h3>Chart B</h3>
          <BirthForm value={birthB} onChange={setBirthB} onSubmit={() => undefined} submitting={false} />
        </div>
      </div>
      <button type="button" onClick={runBoth} disabled={loading}>
        {loading ? "Running both consultations…" : "Run and Compare"}
      </button>
      {error && <p className="fail">{error}</p>}

      {diff && (
        <div className="comparison-results">
          <DiffList title="Claims (by rule card + bound variables)" diff={diff.claims} />
          <DiffList title="Rule cards fired" diff={diff.ruleCards} />
          <DiffList title="Facts" diff={diff.facts} />
          <DiffList title="Contradictions/adjudications" diff={diff.contradictions} />
          <DiffList title="Deferred/unsupported on this chart" diff={diff.deferredOnThisChart} />
          <details>
            <summary>Dasa ordinal differences ({diff.dasaOrdinalDifferences.length})</summary>
            <p className="muted">
              Every chart has the same 9 grahas in its mahadasa sequence; what can differ is
              which position (ordinal) each occupies, since that depends on the birth
              nakshatra.
            </p>
            <ul>
              {diff.dasaOrdinalDifferences.map((d) => (
                <li key={d.graha}>
                  {d.graha}: {d.ordinalA} in A, {d.ordinalB} in B
                </li>
              ))}
            </ul>
          </details>
        </div>
      )}
    </section>
  );
}
