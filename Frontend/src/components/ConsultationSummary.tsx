import type { ConsultResult } from "../types";

interface Props {
  result: ConsultResult;
}

export function ConsultationSummary({ result }: Props) {
  const { chart, claims, coverage, verification } = result;
  const warnings = (chart.resolved_birth.warnings as string[] | undefined) ?? [];
  const deferredCount = coverage.inert_cards.length + coverage.reference_cards.length;

  return (
    <section className="summary-card">
      <h2>Chart Summary</h2>
      <dl className="summary-grid">
        <dt>Birth</dt>
        <dd>
          {String(chart.resolved_birth.date)} {String(chart.resolved_birth.time)} (
          {String(chart.resolved_birth.timezone)}, offset {String(chart.resolved_birth.utc_offset)})
        </dd>

        <dt>Location</dt>
        <dd>
          {String(chart.resolved_birth.place_name) || "(no place name given)"} — lat{" "}
          {String(chart.resolved_birth.latitude)}, lon {String(chart.resolved_birth.longitude)}
        </dd>

        <dt>Reference frame</dt>
        <dd>
          Ascendant {chart.ascendant_sign} ({chart.ascendant.toFixed(4)}°), houses:{" "}
          {chart.houses.system}
        </dd>

        <dt>Calculation metadata</dt>
        <dd>
          bundle {chart.bundle_id.slice(0, 16)}… · engine {chart.engine_version} · ayanamsa{" "}
          {String(chart.settings.ayanamsa)}
        </dd>

        <dt>Claim count</dt>
        <dd>{claims.length}</dd>

        <dt>Warning count</dt>
        <dd className={warnings.length ? "warn" : ""}>
          {warnings.length}
          {warnings.length > 0 && (
            <ul>
              {warnings.map((w, i) => (
                <li key={i}>{w}</li>
              ))}
            </ul>
          )}
        </dd>

        <dt>Deferred/unsupported count (this chart)</dt>
        <dd>{deferredCount}</dd>

        <dt>Verification status</dt>
        <dd className={verification.ok ? "ok" : "fail"}>
          {verification.ok ? "OK — grounded" : "FAILED"}
        </dd>
      </dl>
    </section>
  );
}
