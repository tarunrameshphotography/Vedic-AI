// Mirrors Api/serialize.py, Api/schemas.py, Api/cases.py exactly. This file
// adds no shape of its own -- every field here traces to a real key in a
// real /consult (or /cases, /deferred, /cards/{id}) response. Where the
// engine's own field is untyped JSON (rule_card conditions, deferred.json
// entries), it stays `unknown`/`Record<string, unknown>` here rather than
// inventing a schema the engine itself does not declare.

export interface BirthInput {
  date: string;
  time: string;
  timezone: string;
  latitude: number;
  longitude: number;
  place_name: string;
  name: string;
  time_precision: string;
  time_source: string;
  sex: string;
  ayanamsa: string;
  house_system: string;
}

export const DEFAULT_BIRTH_INPUT: BirthInput = {
  date: "",
  time: "",
  timezone: "",
  latitude: 0,
  longitude: 0,
  place_name: "",
  name: "",
  time_precision: "minute",
  time_source: "unknown",
  sex: "unknown",
  ayanamsa: "lahiri",
  house_system: "whole_sign",
};

export interface BodyState {
  body: string;
  lon: number;
  lat: number;
  speed_lon: number;
  retrograde: boolean;
  sign: string;
  sign_index: number;
  deg_in_sign: number;
  nakshatra: string;
  nakshatra_index: number;
  pada: number;
  house: number;
}

export interface ChartBundle {
  bundle_id: string;
  engine_version: string;
  backend: Record<string, unknown>;
  settings: Record<string, unknown>;
  resolved_birth: Record<string, unknown> & { warnings?: string[] };
  ascendant: number;
  ascendant_sign: string;
  ascendant_sign_index: number;
  midheaven: number;
  houses: { system: string; cusps: number[]; signs: string[] };
  bodies: Record<string, BodyState>;
  invariants_checked: string[];
}

export interface Fact {
  key: string;
  predicate: string;
  args: Record<string, unknown>;
  frame: Record<string, unknown>;
  evidence: Record<string, unknown>;
  stability: string;
}

export interface DoctrineReport {
  consulted: Record<string, string[]>;
  skipped: Record<string, string>;
  partial: Record<string, string>;
  conflicts: Array<Record<string, unknown>>;
}

export interface FactsPayload {
  items: Fact[];
  doctrine: DoctrineReport;
}

export interface ClaimSource {
  book_id: string;
  book_title: string;
  author: string;
  translator: string;
  chapter: number;
  verse: string;
  tier: number;
}

export interface ClaimPassage {
  quote: string;
  quote_display: string | string[];
  corpus_file: string;
  char_span: [number, number];
  spans: Array<[number, number]>;
  quote_sha256: string;
  page_anchor: string | null;
  span_trimmed: string | null;
}

export interface ClaimDerived {
  facts: Array<{ key: string; frame: Record<string, unknown>; evidence: Record<string, unknown> }>;
  rule_card: string;
  conditions_satisfied: string[];
  variables: Record<string, string>;
}

export interface ClaimWindow {
  start: string;
  end: string;
}

export interface Claim {
  claim_id: string;
  astronomical: Record<string, unknown>;
  derived: ClaimDerived;
  source: ClaimSource;
  passage: ClaimPassage;
  weight: number;
  specificity: number;
  tier: number;
  stability: string;
  text: string;
  window: ClaimWindow | null;
}

export type AdjudicationRelationship =
  | "contradiction"
  | "qualification"
  | "parallel_authority"
  | "override";

export type AdjudicationResolution = "applied" | "unresolved" | "recorded";

export interface Party {
  card: string;
  book: string;
  chapter: number;
  verse: string;
  page_anchor: string | null;
  authority: string;
  statement: string;
  activation: string;
  claim_ids: string[];
}

export interface Adjudication {
  subject: string;
  relationship: AdjudicationRelationship;
  resolution: AdjudicationResolution;
  reason: string;
  parties: Party[];
  basis: string[];
  declared_as: string[];
  claim_ids: string[];
}

export interface Sentence {
  text: string;
  claim_ids: string[];
  part: "rules" | "synthesis";
}

export interface Concentration {
  house: number;
  bodies: string[];
  claim_ids: string[];
}

export interface Theme {
  term: string;
  variants: string[];
  occurrences: Array<{ claim_id: string; word: string; negated: boolean; cue: string | null }>;
  doctrinal_conflicts: Array<[string, string]>;
}

export interface SynthesisResult {
  concentrations: Concentration[];
  themes: Theme[];
  method_note: string;
  total_claims: number;
}

export interface Coverage {
  cards_in_store: number;
  candidates_from_index: number;
  claims_activated: number;
  inert_cards: string[];
  out_of_scope: string[];
  reference_cards: string[];
  not_covered: string[];
  loaded_doctrine: string[];
}

export interface VerificationResult {
  ok: boolean;
  checks: Record<string, number | boolean>;
  failures: string[];
}

export interface DasaPeriod {
  graha: string;
  ordinal: number;
  years: number;
  start: string;
  end: string;
  balance_at_birth: boolean;
  claim_ids: string[];
}

export interface ConsultResult {
  chart: ChartBundle;
  facts: FactsPayload;
  claims: Claim[];
  adjudications: Adjudication[];
  sentences: Sentence[];
  synthesis: SynthesisResult;
  coverage: Coverage;
  verification: VerificationResult;
  dasa_timeline: DasaPeriod[];
  consultation: string;
  audit: string;
}

export interface DeferredDependency {
  title: string;
  kind: string;
  predicate?: string;
  detail: string;
  phase: string;
  depends_on: string[];
  effort: number;
  effort_basis: string;
  implemented?: boolean;
}

export interface DeferredEntry {
  id: string;
  kind: "chapter" | "passage" | "concept";
  book?: string;
  chapter?: number;
  locus?: string;
  what: string;
  reason: string;
  requires: string[];
  phase: string;
  status: "deferred" | "resolved";
  paragraphs?: number[];
}

export interface DeferredRegistry {
  schema: number;
  note: string;
  dependencies: Record<string, DeferredDependency>;
  entries: DeferredEntry[];
}

// A rule card's own raw JSON, straight from Rules/<book>/ch<NN>.json --
// intentionally loose: the frontend must never re-interpret this shape, only
// display it, so it is not modelled field-by-field the way engine-derived
// output above is.
export type RuleCardRaw = Record<string, unknown>;

export interface CaseManifest {
  slug: string;
  label: string;
  notes: string;
  birth: BirthInput;
  created_at: string;
}

export interface ApiErrorDetail {
  error_type: string;
  message: string;
}

export class ApiError extends Error {
  status: number;
  errorType: string;

  constructor(status: number, detail: ApiErrorDetail | string) {
    const message = typeof detail === "string" ? detail : detail.message;
    super(message);
    this.status = status;
    this.errorType = typeof detail === "string" ? "unknown" : detail.error_type;
  }
}
