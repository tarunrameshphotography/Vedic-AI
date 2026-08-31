import type { VerificationResult } from "../types";

interface Props {
  verification: VerificationResult;
}

/** §15: verification failures must be visually unmistakable, never styled
 * to look like a soft warning. A `false` here means the engine itself would
 * have refused to emit this report (Engine.pipeline.run raises rather than
 * returning), so in practice this banner is only ever seen green from a
 * live /consult call -- it stays this explicit anyway, because the API
 * layer's own error-mapping path (verification_failure, 500) is the other
 * place this same failure surfaces. */
export function VerificationView({ verification }: Props) {
  return (
    <section>
      <h2>Verification</h2>
      <div className={`verification-banner ${verification.ok ? "ok" : "fail"}`} role="status">
        {verification.ok ? "✓ GROUNDED — every check passed" : "✗ VERIFICATION FAILED"}
      </div>

      <table className="checks-table">
        <thead>
          <tr>
            <th>Check</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(verification.checks).map(([k, v]) => (
            <tr key={k}>
              <td>{k}</td>
              <td>{String(v)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {verification.failures.length > 0 && (
        <div className="failures">
          <h3>Failures ({verification.failures.length})</h3>
          <ul>
            {verification.failures.map((f, i) => (
              <li key={i} className="fail">{f}</li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
