import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { DasaTimeline } from "../components/DasaTimeline";
import type { Claim, DasaPeriod } from "../types";

const GRAHAS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"];

function makeTimeline(): DasaPeriod[] {
  return GRAHAS.map((graha, i) => ({
    graha,
    ordinal: i + 1,
    years: 10,
    start: `19${87 + i}-01-01T00:00:00Z`,
    end: `19${88 + i}-01-01T00:00:00Z`,
    balance_at_birth: i === 0,
    claim_ids: graha === "Venus" ? ["clm-0001"] : [],
  }));
}

function makeClaims(): Claim[] {
  return [
    {
      claim_id: "clm-0001",
      astronomical: {},
      derived: { facts: [], rule_card: "PD.20.WealthDasa.Venus", conditions_satisfied: [], variables: {} },
      source: { book_id: "phaladeepika", book_title: "Phaladeepika", author: "", translator: "", chapter: 20, verse: "26", tier: 1 },
      passage: { quote: "q", quote_display: "q", corpus_file: "x", char_span: [0, 1], spans: [[0, 1]], quote_sha256: "abc", page_anchor: null, span_trimmed: null },
      weight: 1, specificity: 1, tier: 1, stability: "stable",
      text: "Wealth during Venus mahadasa", window: { start: "1988-01-01T00:00:00Z", end: "1989-01-01T00:00:00Z" },
    },
  ];
}

describe("DasaTimeline", () => {
  it("renders all nine mahadasa periods", () => {
    render(<DasaTimeline timeline={makeTimeline()} claims={makeClaims()} />);
    for (const graha of GRAHAS) {
      expect(screen.getByText(graha)).toBeInTheDocument();
    }
  });

  it("labels Antardasa explicitly as unimplemented rather than omitting it", () => {
    render(<DasaTimeline timeline={makeTimeline()} claims={makeClaims()} />);
    expect(screen.getByText(/not implemented — deferred/i)).toBeInTheDocument();
  });

  it("shows the attached claim when a period is selected", () => {
    render(<DasaTimeline timeline={makeTimeline()} claims={makeClaims()} />);
    fireEvent.click(screen.getByText("Venus"));
    expect(screen.getByText(/Wealth during Venus mahadasa/)).toBeInTheDocument();
  });

  it("shows no-claims message for a period with none attached", () => {
    render(<DasaTimeline timeline={makeTimeline()} claims={makeClaims()} />);
    fireEvent.click(screen.getByText("Ketu"));
    expect(screen.getByText(/No claims from the current rule store fire/)).toBeInTheDocument();
  });
});
