import { useEffect, useState } from "react";
import { getDeferred } from "../api";
import { ApiError, type Coverage, type DeferredRegistry } from "../types";

interface Props {
  coverage: Coverage;
}

/** §12: four genuinely different kinds of silence, never merged into one
 * invented status.
 *
 *  - "Not triggered": a card whose conditions the store can evaluate, but
 *    which simply came out false on this chart (absent from claims, and
 *    absent from every list below).
 *  - "Not computable": `coverage.inert_cards` -- declared inert because a
 *    predicate the card needs is not yet derivable by this engine.
 *  - "Reference only": `coverage.reference_cards` -- doctrine the engine
 *    reads (a lordship table, an exaltation table) and never asserts as a
 *    claim about a nativity.
 *  - "Source unresolved": the repository-wide `Rules/deferred.json`
 *    registry, read as-is -- its own `reason` text says why, verbatim, and
 *    is never reclassified into a status the entry itself does not claim.
 *
 * `not_covered` (bodies in a house with no rule card in the store at all) is
 * shown separately again: it is not even "not triggered", it is corpus
 * silence -- the store never spoke to that placement.
 */
export function DeferredView({ coverage }: Props) {
  const [registry, setRegistry] = useState<DeferredRegistry | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<"all" | "deferred" | "resolved">("deferred");

  useEffect(() => {
    getDeferred()
      .then(setRegistry)
      .catch((e: unknown) => setError(e instanceof ApiError ? e.message : String(e)));
  }, []);

  const entries = registry?.entries.filter(
    (e) => statusFilter === "all" || e.status === statusFilter,
  );

  return (
    <section>
      <h2>Deferred / Unsupported Doctrine</h2>

      <div className="deferred-section">
        <h3>This chart — not computable ({coverage.inert_cards.length})</h3>
        <p className="muted">
          Cards recorded but declared inert: a predicate the condition needs is not yet
          derivable by this engine. Knowledge on record, not yet a rule.
        </p>
        <ul>
          {coverage.inert_cards.map((line, i) => (
            <li key={i}>{line}</li>
          ))}
        </ul>
      </div>

      <div className="deferred-section">
        <h3>This chart — reference only ({coverage.reference_cards.length})</h3>
        <p className="muted">
          Doctrine the engine reads (a lordship table, an exaltation table) and never
          asserts as a claim about a nativity.
        </p>
        <ul>
          {coverage.reference_cards.map((line, i) => (
            <li key={i}>{line}</li>
          ))}
        </ul>
      </div>

      <div className="deferred-section">
        <h3>This chart — corpus silence ({coverage.not_covered.length})</h3>
        <p className="muted">
          A placement with no rule card in the store at all. The absence of a claim is
          not evidence the underlying proposition is false — the texts have not been
          consulted on it.
        </p>
        <ul>
          {coverage.not_covered.map((line, i) => (
            <li key={i}>{line}</li>
          ))}
        </ul>
      </div>

      <div className="deferred-section">
        <h3>Repository-wide — source unresolved / not yet built</h3>
        {error && <p className="fail">Could not load /deferred: {error}</p>}
        {registry && (
          <>
            <label>
              Status:{" "}
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value as "all" | "deferred" | "resolved")}
              >
                <option value="deferred">deferred</option>
                <option value="resolved">resolved</option>
                <option value="all">all ({registry.entries.length})</option>
              </select>
            </label>
            <p className="muted">{entries?.length ?? 0} entries shown, verbatim from Rules/deferred.json</p>
            <ul className="deferred-entries">
              {entries?.map((e) => (
                <li key={e.id}>
                  <details>
                    <summary>
                      <code>{e.id}</code> ({e.kind}) — {e.what}
                    </summary>
                    <p>{e.reason}</p>
                    {e.requires.length > 0 && (
                      <p className="muted">
                        Requires:{" "}
                        {e.requires.map((r) => {
                          const dep = registry.dependencies[r];
                          return `${r}${dep ? ` [${dep.implemented ? "implemented" : "not implemented"}]` : ""}`;
                        }).join(", ")}
                      </p>
                    )}
                  </details>
                </li>
              ))}
            </ul>
          </>
        )}
      </div>
    </section>
  );
}
