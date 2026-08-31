import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ClaimsExplorer } from "../components/ClaimsExplorer";
import type { Claim, VerificationResult } from "../types";

function makeClaims(): Claim[] {
  return [
    {
      claim_id: "clm-0001",
      astronomical: {},
      derived: { facts: [], rule_card: "PD.20.WealthDasa.Venus", conditions_satisfied: ["dignity(Venus,exalted)"], variables: {} },
      source: { book_id: "phaladeepika", book_title: "Phaladeepika", author: "", translator: "", chapter: 20, verse: "26", tier: 1 },
      passage: { quote: "q", quote_display: "Venus produces wealth", corpus_file: "x", char_span: [0, 1], spans: [[0, 1]], quote_sha256: "abc", page_anchor: "p0186", span_trimmed: null },
      weight: 1, specificity: 1, tier: 1, stability: "stable",
      text: "Wealth during Venus mahadasa", window: { start: "1988-01-01T00:00:00Z", end: "1989-01-01T00:00:00Z" },
    },
  ];
}

const OK: VerificationResult = { ok: true, checks: {}, failures: [] };

describe("ClaimsExplorer", () => {
  it("renders the claim collapsed, showing rule card and text", () => {
    const { container } = render(<ClaimsExplorer claims={makeClaims()} verification={OK} />);
    const summary = container.querySelector("summary")!;
    expect(summary).toHaveTextContent("PD.20.WealthDasa.Venus");
    expect(summary).toHaveTextContent("Wealth during Venus mahadasa");
  });

  it("expands to show the provenance panel when its summary is clicked", () => {
    const { container } = render(<ClaimsExplorer claims={makeClaims()} verification={OK} />);
    const details = container.querySelector("details")!;
    const summary = container.querySelector("summary")!;
    expect(details.open).toBe(false);
    fireEvent.click(summary);
    expect(details.open).toBe(true);
    expect(screen.getByText("Exact quote")).toBeInTheDocument();
  });

  it("filters the list down when a non-matching filter is typed", () => {
    render(<ClaimsExplorer claims={makeClaims()} verification={OK} />);
    fireEvent.change(screen.getByLabelText(/filter claims/i), { target: { value: "nonexistent-xyz" } });
    expect(screen.getByText(/No claims match this filter/)).toBeInTheDocument();
  });

  it("flags a claim whose id appears in verification failures", () => {
    const failing: VerificationResult = { ok: false, checks: {}, failures: ["clm-0001: quote hash mismatch"] };
    render(<ClaimsExplorer claims={makeClaims()} verification={failing} />);
    expect(screen.getByText(/verification failed/i)).toBeInTheDocument();
  });
});
