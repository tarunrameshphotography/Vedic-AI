import { useEffect, useState } from "react";
import { getCard } from "../api";
import { ApiError, type RuleCardRaw } from "../types";

interface Props {
  cardId: string;
}

/** For a selected claim: the raw rule card straight from Rules/<book>/ch<NN>.json
 * -- condition tree, satisfied-conditions vocabulary, scope, predicts -- read
 * directly, never re-interpreted. GET /cards/{id} is a passthrough of the
 * same file the engine itself loads. */
export function RuleInspector({ cardId }: Props) {
  const [card, setCard] = useState<RuleCardRaw | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    getCard(cardId)
      .then((c) => !cancelled && setCard(c))
      .catch((e: unknown) => !cancelled && setError(e instanceof ApiError ? e.message : String(e)))
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
  }, [cardId]);

  if (loading) return <p>Loading rule card {cardId}…</p>;
  if (error) return <p className="fail">Could not load {cardId}: {error}</p>;
  if (!card) return null;

  return (
    <div className="rule-inspector">
      <dl className="summary-grid">
        <dt>Card ID</dt>
        <dd>{String(card.id)}</dd>
        <dt>Activation</dt>
        <dd>{String(card.activation ?? "active")}</dd>
        <dt>Weight / specificity</dt>
        <dd>
          {String(card.weight ?? 1)} / {String(card.specificity ?? 1)}
        </dd>
        <dt>Timing</dt>
        <dd>{String(card.timing ?? "natal")}</dd>
      </dl>

      <details open>
        <summary>Scope</summary>
        <pre>{JSON.stringify(card.scope ?? {}, null, 2)}</pre>
      </details>
      <details open>
        <summary>Condition tree</summary>
        <pre>{JSON.stringify(card.conditions ?? {}, null, 2)}</pre>
      </details>
      <details>
        <summary>Predicts</summary>
        <pre>{JSON.stringify(card.predicts ?? {}, null, 2)}</pre>
      </details>
      <details>
        <summary>Relationship links (contradicts / extends / parallel_of)</summary>
        <pre>
          {JSON.stringify(
            {
              contradicts: card.contradicts ?? [],
              extends: card.extends ?? [],
              parallel_of: card.parallel_of ?? [],
            },
            null,
            2,
          )}
        </pre>
      </details>
    </div>
  );
}
