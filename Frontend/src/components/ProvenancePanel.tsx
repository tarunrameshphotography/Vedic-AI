import type { Claim } from "../types";

interface Props {
  claim: Claim;
}

/** The full source -> passage -> condition -> facts -> claim -> timing chain
 * (master prompt §9/§20), read entirely off one Claim -- nothing here is
 * derived, only displayed. */
export function ProvenancePanel({ claim }: Props) {
  const quote = Array.isArray(claim.passage.quote_display)
    ? claim.passage.quote_display.join(" […] ")
    : claim.passage.quote_display;

  return (
    <div className="provenance-panel">
      <section>
        <h4>Source</h4>
        <dl className="summary-grid">
          <dt>Book</dt>
          <dd>{claim.source.book_title} ({claim.source.book_id})</dd>
          <dt>Author / translator</dt>
          <dd>
            {claim.source.author || "—"}
            {claim.source.translator ? ` / ${claim.source.translator}` : ""}
          </dd>
          <dt>Chapter / verse</dt>
          <dd>
            ch. {claim.source.chapter}, v. {claim.source.verse}
          </dd>
          <dt>Page anchor</dt>
          <dd>{claim.passage.page_anchor ?? "—"}</dd>
          <dt>Tier</dt>
          <dd>{claim.source.tier}</dd>
        </dl>
      </section>

      <section>
        <h4>Exact quote</h4>
        <blockquote>{quote}</blockquote>
        <p className="muted">sha256: {claim.passage.quote_sha256}</p>
      </section>

      <section>
        <h4>Condition / satisfied facts</h4>
        <p>Rule card: <code>{claim.derived.rule_card}</code></p>
        <ul>
          {claim.derived.conditions_satisfied.map((k) => (
            <li key={k}><code>{k}</code></li>
          ))}
        </ul>
        {Object.keys(claim.derived.variables).length > 0 && (
          <p>
            Bound variables:{" "}
            {Object.entries(claim.derived.variables)
              .map(([k, v]) => `${k} = ${v}`)
              .join(", ")}
          </p>
        )}
      </section>

      <section>
        <h4>Timing</h4>
        {claim.window ? (
          <p>
            Mahadasa window: <strong>{claim.window.start}</strong> to{" "}
            <strong>{claim.window.end}</strong>
          </p>
        ) : (
          <p>Timeless (not a dasa-scoped claim).</p>
        )}
      </section>

      <section>
        <h4>Weight / specificity / stability</h4>
        <p>
          weight {claim.weight}, specificity {claim.specificity}, stability {claim.stability}
        </p>
      </section>
    </div>
  );
}
