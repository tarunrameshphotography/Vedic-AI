import { describe, expect, it } from "vitest";
import { claimSignature, diffConsultations } from "../components/ComparisonMode";
import type { Claim, ConsultResult } from "../types";

function makeClaim(overrides: Partial<Claim>): Claim {
  return {
    claim_id: "clm-0001",
    astronomical: {},
    derived: { facts: [], rule_card: "PD.TEST.Card", conditions_satisfied: [], variables: {} },
    source: { book_id: "phaladeepika", book_title: "Phaladeepika", author: "", translator: "", chapter: 1, verse: "1", tier: 1 },
    passage: { quote: "q", quote_display: "q", corpus_file: "x", char_span: [0, 1], spans: [[0, 1]], quote_sha256: "abc", page_anchor: null, span_trimmed: null },
    weight: 1,
    specificity: 1,
    tier: 1,
    stability: "stable",
    text: "some claim text",
    window: null,
    ...overrides,
  };
}

function makeResult(overrides: Partial<ConsultResult>): ConsultResult {
  return {
    chart: {} as ConsultResult["chart"],
    facts: { items: [], doctrine: { consulted: {}, skipped: {}, partial: {}, conflicts: [] } },
    claims: [],
    adjudications: [],
    sentences: [],
    synthesis: { concentrations: [], themes: [], method_note: "", total_claims: 0 },
    coverage: {
      cards_in_store: 0, candidates_from_index: 0, claims_activated: 0,
      inert_cards: [], out_of_scope: [], reference_cards: [], not_covered: [], loaded_doctrine: [],
    },
    verification: { ok: true, checks: {}, failures: [] },
    dasa_timeline: [],
    consultation: "",
    audit: "",
    ...overrides,
  };
}

describe("claimSignature", () => {
  it("is stable regardless of the arbitrary sequential claim_id", () => {
    const a = makeClaim({ claim_id: "clm-0001", derived: { facts: [], rule_card: "PD.X", conditions_satisfied: [], variables: { g: "Venus" } } });
    const b = makeClaim({ claim_id: "clm-0099", derived: { facts: [], rule_card: "PD.X", conditions_satisfied: [], variables: { g: "Venus" } } });
    expect(claimSignature(a)).toBe(claimSignature(b));
  });

  it("differs when the bound variable differs (different graha satisfied it)", () => {
    const venus = makeClaim({ derived: { facts: [], rule_card: "PD.X", conditions_satisfied: [], variables: { g: "Venus" } } });
    const mars = makeClaim({ derived: { facts: [], rule_card: "PD.X", conditions_satisfied: [], variables: { g: "Mars" } } });
    expect(claimSignature(venus)).not.toBe(claimSignature(mars));
  });
});

describe("diffConsultations", () => {
  it("never ranks -- output has no ordering/score field, only set membership", () => {
    const a = makeResult({ claims: [makeClaim({ derived: { facts: [], rule_card: "PD.A", conditions_satisfied: [], variables: {} } })] });
    const b = makeResult({ claims: [makeClaim({ derived: { facts: [], rule_card: "PD.B", conditions_satisfied: [], variables: {} } })] });
    const diff = diffConsultations(a, b);
    expect(Object.keys(diff)).toEqual([
      "claims", "ruleCards", "facts", "contradictions", "deferredOnThisChart", "dasaOrdinalDifferences",
    ]);
    expect(diff.claims.onlyA).toEqual(["PD.A"]);
    expect(diff.claims.onlyB).toEqual(["PD.B"]);
    expect(diff.claims.shared).toEqual([]);
  });

  it("finds shared claims by signature, not by claim_id", () => {
    const shared = { rule_card: "PD.SHARED", conditions_satisfied: [], facts: [], variables: {} };
    const a = makeResult({ claims: [makeClaim({ claim_id: "clm-0001", derived: shared })] });
    const b = makeResult({ claims: [makeClaim({ claim_id: "clm-0042", derived: shared })] });
    const diff = diffConsultations(a, b);
    expect(diff.claims.shared).toEqual(["PD.SHARED"]);
    expect(diff.claims.onlyA).toEqual([]);
    expect(diff.claims.onlyB).toEqual([]);
  });

  it("diffs facts by key", () => {
    const a = makeResult({ facts: { items: [{ key: "in_house(Venus,10)", predicate: "in_house", args: {}, frame: {}, evidence: {}, stability: "stable" }], doctrine: { consulted: {}, skipped: {}, partial: {}, conflicts: [] } } });
    const b = makeResult({ facts: { items: [{ key: "in_house(Mars,7)", predicate: "in_house", args: {}, frame: {}, evidence: {}, stability: "stable" }], doctrine: { consulted: {}, skipped: {}, partial: {}, conflicts: [] } } });
    const diff = diffConsultations(a, b);
    expect(diff.facts.onlyA).toEqual(["in_house(Venus,10)"]);
    expect(diff.facts.onlyB).toEqual(["in_house(Mars,7)"]);
  });

  it("reports dasa ordinal differences only where the graha's position actually differs", () => {
    const a = makeResult({
      dasa_timeline: [
        { graha: "Venus", ordinal: 1, years: 20, start: "x", end: "y", balance_at_birth: true, claim_ids: [] },
        { graha: "Sun", ordinal: 2, years: 6, start: "x", end: "y", balance_at_birth: false, claim_ids: [] },
      ],
    });
    const b = makeResult({
      dasa_timeline: [
        { graha: "Venus", ordinal: 3, years: 20, start: "x", end: "y", balance_at_birth: false, claim_ids: [] },
        { graha: "Sun", ordinal: 2, years: 6, start: "x", end: "y", balance_at_birth: false, claim_ids: [] },
      ],
    });
    const diff = diffConsultations(a, b);
    expect(diff.dasaOrdinalDifferences).toEqual([{ graha: "Venus", ordinalA: 1, ordinalB: 3 }]);
  });
});
