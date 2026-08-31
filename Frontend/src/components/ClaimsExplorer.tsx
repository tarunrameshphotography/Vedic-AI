import { useState } from "react";
import type { Claim, VerificationResult } from "../types";
import { ProvenancePanel } from "./ProvenancePanel";
import { RuleInspector } from "./RuleInspector";

interface Props {
  claims: Claim[];
  verification: VerificationResult;
}

/** §7/§8: every claim, collapsed to its rule-card id and prediction text,
 * expandable (native <details>/<summary> -- keyboard-accessible for free)
 * into the full source/condition/timing/rule-card view. Nothing here is
 * natural-language explanation invented beyond the engine's own `text`. */
export function ClaimsExplorer({ claims, verification }: Props) {
  const [filter, setFilter] = useState("");
  const [showRule, setShowRule] = useState<Record<string, boolean>>({});

  const failedIds = new Set(
    verification.failures.flatMap((f) => {
      const m = /^(clm-\d+)/.exec(f);
      return m ? [m[1]] : [];
    }),
  );

  const filtered = claims.filter((c) => {
    const needle = filter.trim().toLowerCase();
    if (!needle) return true;
    return (
      c.claim_id.toLowerCase().includes(needle) ||
      c.derived.rule_card.toLowerCase().includes(needle) ||
      c.text.toLowerCase().includes(needle)
    );
  });

  return (
    <section>
      <h2>Claims ({claims.length})</h2>
      <input
        type="search"
        placeholder="Filter by claim id, rule card, or text…"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        aria-label="Filter claims"
      />
      {filtered.length === 0 && <p>No claims match this filter.</p>}
      <ul className="claims-list">
        {filtered.map((c) => (
          <li key={c.claim_id}>
            <details>
              <summary>
                <code>{c.derived.rule_card}</code>
                {" — "}
                {c.text}
                {c.window && <span className="badge">dasa-timed</span>}
                {failedIds.has(c.claim_id) && <span className="badge fail">verification failed</span>}
              </summary>
              <div className="claim-detail">
                <ProvenancePanel claim={c} />
                <button
                  type="button"
                  onClick={() =>
                    setShowRule((prev) => ({ ...prev, [c.claim_id]: !prev[c.claim_id] }))
                  }
                >
                  {showRule[c.claim_id] ? "Hide rule card" : "Inspect rule card"}
                </button>
                {showRule[c.claim_id] && <RuleInspector cardId={c.derived.rule_card} />}
              </div>
            </details>
          </li>
        ))}
      </ul>
    </section>
  );
}
