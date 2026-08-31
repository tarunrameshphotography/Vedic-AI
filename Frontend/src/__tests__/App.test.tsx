import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import App from "../App";

function jsonResponse(status: number, body: unknown): Response {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
  } as Response;
}

const MINIMAL_RESULT = {
  chart: {
    bundle_id: "sha256:abc", engine_version: "0.1.0", backend: {}, settings: { ayanamsa: "lahiri" },
    resolved_birth: { date: "1987-03-14", time: "04:22", timezone: "Asia/Kolkata", utc_offset: "+05:30", place_name: "Thanjavur", latitude: 10.787, longitude: 79.1378, warnings: [] },
    ascendant: 12.3, ascendant_sign: "Aries", ascendant_sign_index: 0, midheaven: 90,
    houses: { system: "whole_sign", cusps: [], signs: Array(12).fill("Aries") },
    bodies: {}, invariants_checked: [],
  },
  facts: { items: [], doctrine: { consulted: {}, skipped: {}, partial: {}, conflicts: [] } },
  claims: [],
  adjudications: [],
  sentences: [],
  synthesis: { concentrations: [], themes: [], method_note: "", total_claims: 0 },
  coverage: { cards_in_store: 0, candidates_from_index: 0, claims_activated: 0, inert_cards: [], out_of_scope: [], reference_cards: [], not_covered: [], loaded_doctrine: [] },
  verification: { ok: true, checks: {}, failures: [] },
  dasa_timeline: [],
  consultation: "text", audit: "text",
};

const VALID_BIRTH = {
  date: "1987-03-14", time: "04:22", timezone: "Asia/Kolkata",
  latitude: "10.787", longitude: "79.1378",
};

function fillAndSubmit() {
  fireEvent.change(screen.getByLabelText(/Date/), { target: { value: VALID_BIRTH.date } });
  fireEvent.change(screen.getByLabelText(/Time \(HH/), { target: { value: VALID_BIRTH.time } });
  fireEvent.change(screen.getByLabelText(/Timezone/), { target: { value: VALID_BIRTH.timezone } });
  fireEvent.change(screen.getByLabelText(/Latitude/), { target: { value: VALID_BIRTH.latitude } });
  fireEvent.change(screen.getByLabelText(/Longitude/), { target: { value: VALID_BIRTH.longitude } });
  // Two buttons share this name: the nav tab and the form's own submit
  // button. Only the submit button actually runs the consultation.
  const submit = screen
    .getAllByRole("button", { name: /run consultation/i })
    .find((b) => b.getAttribute("type") === "submit")!;
  fireEvent.click(submit);
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("App", () => {
  it("shows a loading state, then the consultation summary on success", async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, MINIMAL_RESULT));
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);
    fillAndSubmit();

    expect(screen.getByRole("button", { name: /running consultation/i })).toBeDisabled();

    await waitFor(() => expect(screen.getByText("Chart Summary")).toBeInTheDocument());
    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringContaining("/consult"),
      expect.objectContaining({ method: "POST" }),
    );
  });

  it("shows the API's real error message verbatim on failure, never a paraphrase", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      jsonResponse(400, { detail: { error_type: "invalid_input", message: "unknown IANA time zone 'Not/AZone'" } }),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);
    fillAndSubmit();

    await waitFor(() =>
      expect(screen.getByRole("alert")).toHaveTextContent("unknown IANA time zone 'Not/AZone'"),
    );
  });

  it("disables result-dependent tabs until a consultation has run", () => {
    render(<App />);
    expect(screen.getByRole("button", { name: "Claims" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Dasa Timeline" })).toBeDisabled();
  });
});
