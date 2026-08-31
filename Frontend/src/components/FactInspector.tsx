import { useState } from "react";
import type { FactsPayload } from "../types";

interface Props {
  facts: FactsPayload;
}

/** §13: the actual extracted FactSet, filterable, plus what each doctrine-
 * backed extractor consulted/skipped/read-partially/found-in-conflict --
 * `FactSet.doctrine`, read directly, never recomputed. */
export function FactInspector({ facts }: Props) {
  const [filter, setFilter] = useState("");

  const filtered = facts.items.filter((f) => {
    const needle = filter.trim().toLowerCase();
    if (!needle) return true;
    return f.key.toLowerCase().includes(needle) || f.predicate.toLowerCase().includes(needle);
  });

  return (
    <section>
      <h2>Facts ({facts.items.length})</h2>
      <input
        type="search"
        placeholder="Filter by predicate or key…"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        aria-label="Filter facts"
      />
      <table className="facts-table">
        <thead>
          <tr>
            <th>Key</th>
            <th>Predicate</th>
            <th>Args</th>
            <th>Stability</th>
            <th>Evidence</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map((f) => (
            <tr key={f.key}>
              <td><code>{f.key}</code></td>
              <td>{f.predicate}</td>
              <td>{JSON.stringify(f.args)}</td>
              <td>{f.stability}</td>
              <td>
                <details>
                  <summary>evidence</summary>
                  <pre>{JSON.stringify(f.evidence, null, 2)}</pre>
                </details>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Doctrine report</h3>
      <details open>
        <summary>Consulted ({Object.keys(facts.doctrine.consulted).length} extractors)</summary>
        <pre>{JSON.stringify(facts.doctrine.consulted, null, 2)}</pre>
      </details>
      <details>
        <summary>Skipped ({Object.keys(facts.doctrine.skipped).length})</summary>
        <pre>{JSON.stringify(facts.doctrine.skipped, null, 2)}</pre>
      </details>
      <details>
        <summary>Partial ({Object.keys(facts.doctrine.partial).length})</summary>
        <pre>{JSON.stringify(facts.doctrine.partial, null, 2)}</pre>
      </details>
      <details>
        <summary>Conflicts ({facts.doctrine.conflicts.length})</summary>
        <pre>{JSON.stringify(facts.doctrine.conflicts, null, 2)}</pre>
      </details>
    </section>
  );
}
