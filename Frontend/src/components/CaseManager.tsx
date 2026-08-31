import { useEffect, useState } from "react";
import { listCases, saveCase } from "../api";
import { ApiError, type BirthInput, type CaseManifest } from "../types";

interface Props {
  currentBirth: BirthInput;
  onLoad: (birth: BirthInput) => void;
}

/** §17: save/reopen local test charts under Cases/<slug>/chart.json. Never
 * uploaded anywhere; Cases/ is entirely .gitignore'd already. */
export function CaseManager({ currentBirth, onLoad }: Props) {
  const [cases, setCases] = useState<CaseManifest[]>([]);
  const [label, setLabel] = useState("");
  const [notes, setNotes] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  function refresh() {
    listCases()
      .then(setCases)
      .catch((e: unknown) => setError(e instanceof ApiError ? e.message : String(e)));
  }

  useEffect(refresh, []);

  async function handleSave() {
    setError(null);
    setSaving(true);
    try {
      await saveCase(label, notes, currentBirth);
      setLabel("");
      setNotes("");
      refresh();
    } catch (e) {
      setError(e instanceof ApiError ? e.message : String(e));
    } finally {
      setSaving(false);
    }
  }

  return (
    <section>
      <h2>Saved Test Charts</h2>

      <div className="case-save">
        <label>
          Label
          <input value={label} onChange={(e) => setLabel(e.target.value)} />
        </label>
        <label>
          Notes
          <input value={notes} onChange={(e) => setNotes(e.target.value)} />
        </label>
        <button type="button" disabled={!label.trim() || saving} onClick={handleSave}>
          {saving ? "Saving…" : "Save current birth data as a test chart"}
        </button>
      </div>

      {error && <p className="fail">{error}</p>}

      {cases.length === 0 ? (
        <p>No saved test charts yet.</p>
      ) : (
        <ul className="case-list">
          {cases.map((c) => (
            <li key={c.slug}>
              <strong>{c.label}</strong> ({c.slug}) — {c.birth.date} {c.birth.time}{" "}
              {c.birth.timezone}
              {c.notes && <em> — {c.notes}</em>}
              <button type="button" onClick={() => onLoad(c.birth)}>
                Load into form
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
