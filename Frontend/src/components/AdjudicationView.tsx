import type { Adjudication, AdjudicationResolution } from "../types";

interface Props {
  adjudications: Adjudication[];
}

const GROUP_ORDER: AdjudicationResolution[] = ["unresolved", "applied", "recorded"];
const GROUP_LABEL: Record<AdjudicationResolution, string> = {
  unresolved: "Unresolved — both statements stand, the corpus ranks neither",
  applied: "Applied — the source itself states which claim gives way",
  recorded: "Recorded — the other side is on record but not a claim on this chart",
};

/** §11: every contradicts/extends/parallel_of relationship the store
 * declares and this chart's facts activate, grouped unresolved-first,
 * matching Engine.adjudicate's own ordering. No authority weighting is
 * added here -- the engine deliberately has none, and neither does this
 * view. */
export function AdjudicationView({ adjudications }: Props) {
  if (adjudications.length === 0) {
    return (
      <section>
        <h2>Adjudications</h2>
        <p>No declared relationship between cards is activated by this chart.</p>
      </section>
    );
  }

  return (
    <section>
      <h2>Adjudications ({adjudications.length})</h2>
      {GROUP_ORDER.map((resolution) => {
        const group = adjudications.filter((a) => a.resolution === resolution);
        if (group.length === 0) return null;
        return (
          <div key={resolution} className="adjudication-group">
            <h3>{GROUP_LABEL[resolution]} ({group.length})</h3>
            <ul>
              {group.map((a, i) => (
                <li key={`${a.subject}-${i}`}>
                  <details>
                    <summary>
                      <span className="badge">{a.relationship}</span> {a.subject}
                    </summary>
                    <p>{a.reason}</p>
                    {a.basis.length > 0 && (
                      <p className="muted">Basis: {a.basis.join(", ")}</p>
                    )}
                    <table className="parties-table">
                      <thead>
                        <tr>
                          <th>Card</th>
                          <th>Book</th>
                          <th>Ch./v.</th>
                          <th>Authority</th>
                          <th>Statement</th>
                          <th>Activated on this chart</th>
                        </tr>
                      </thead>
                      <tbody>
                        {a.parties.map((p) => (
                          <tr key={p.card}>
                            <td><code>{p.card}</code></td>
                            <td>{p.book}</td>
                            <td>{p.chapter}.{p.verse}</td>
                            <td>{p.authority || "—"}</td>
                            <td>{p.statement}</td>
                            <td>{p.claim_ids.length > 0 ? p.claim_ids.join(", ") : "no"}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </details>
                </li>
              ))}
            </ul>
          </div>
        );
      })}
    </section>
  );
}
