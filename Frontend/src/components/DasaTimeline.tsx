import { useState } from "react";
import type { Claim, DasaPeriod } from "../types";

interface Props {
  timeline: DasaPeriod[];
  claims: Claim[];
}

/** §10: the 9 mahadasa periods, click-through to the claims attached to
 * each. Antardasa is explicitly labelled unsupported/deferred rather than
 * silently absent -- no sub-period arithmetic is printed anywhere in the
 * encoded source, so none is invented here either. */
export function DasaTimeline({ timeline, claims }: Props) {
  const [selected, setSelected] = useState<string | null>(null);
  const claimsById = new Map(claims.map((c) => [c.claim_id, c]));
  const active = timeline.find((p) => p.graha === selected);

  return (
    <section>
      <h2>Vimshottari Mahadasa Timeline</h2>
      <p className="muted">
        Mahadasa only. Antardasa is <strong>not implemented — deferred</strong>: no
        sub-period order or duration arithmetic is printed anywhere in the encoded source
        (chapters 19–20), so none is computed or estimated here.
      </p>
      <table className="dasa-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Graha</th>
            <th>Years</th>
            <th>Start</th>
            <th>End</th>
            <th>Balance at birth</th>
            <th>Claims</th>
          </tr>
        </thead>
        <tbody>
          {timeline.map((p) => (
            <tr
              key={p.graha}
              className={selected === p.graha ? "selected" : ""}
              onClick={() => setSelected(p.graha === selected ? null : p.graha)}
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  setSelected(p.graha === selected ? null : p.graha);
                }
              }}
            >
              <td>{p.ordinal}</td>
              <td>{p.graha}</td>
              <td>{p.years}</td>
              <td>{p.start}</td>
              <td>{p.end}</td>
              <td>{p.balance_at_birth ? "yes" : "no"}</td>
              <td>{p.claim_ids.length}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {active && (
        <div className="dasa-detail">
          <h3>{active.graha} mahadasa — claims</h3>
          {active.claim_ids.length === 0 ? (
            <p>No claims from the current rule store fire during this period.</p>
          ) : (
            <ul>
              {active.claim_ids.map((id) => {
                const c = claimsById.get(id);
                return (
                  <li key={id}>
                    <code>{c?.derived.rule_card ?? id}</code> — {c?.text ?? "(claim not found)"}
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      )}
    </section>
  );
}
