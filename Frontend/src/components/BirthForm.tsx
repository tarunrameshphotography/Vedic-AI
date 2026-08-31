import { useState, type FormEvent } from "react";
import { DEFAULT_BIRTH_INPUT, type BirthInput } from "../types";

interface Props {
  value: BirthInput;
  onChange: (value: BirthInput) => void;
  onSubmit: (value: BirthInput) => void;
  submitting: boolean;
}

const REQUIRED_FIELDS: Array<keyof BirthInput> = ["date", "time", "timezone"];

export function BirthForm({ value, onChange, onSubmit, submitting }: Props) {
  const [touched, setTouched] = useState(false);

  function field<K extends keyof BirthInput>(key: K, cast: (raw: string) => BirthInput[K]) {
    return (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
      onChange({ ...value, [key]: cast(e.target.value) });
    };
  }

  const missing = REQUIRED_FIELDS.filter((k) => !String(value[k]).trim());
  const latValid = value.latitude >= -90 && value.latitude <= 90;
  const lonValid = value.longitude >= -180 && value.longitude <= 180;

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setTouched(true);
    // Client-side check is presence/range only -- never a correction. The
    // API's own validation (BirthDataError: unknown zone, DST gap/ambiguity)
    // is the real authority and its message is shown verbatim on failure.
    if (missing.length === 0 && latValid && lonValid) {
      onSubmit(value);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="birth-form" noValidate>
      <div className="field-grid">
        <label>
          Date (YYYY-MM-DD)
          <input
            type="text"
            value={value.date}
            onChange={field("date", (v) => v)}
            placeholder="1987-03-14"
          />
        </label>
        <label>
          Time (HH:MM[:SS])
          <input
            type="text"
            value={value.time}
            onChange={field("time", (v) => v)}
            placeholder="04:22"
          />
        </label>
        <label>
          Timezone (IANA)
          <input
            type="text"
            value={value.timezone}
            onChange={field("timezone", (v) => v)}
            placeholder="Asia/Kolkata"
          />
        </label>
        <label>
          Latitude (north+)
          <input
            type="number"
            step="any"
            value={value.latitude}
            onChange={field("latitude", (v) => Number(v))}
          />
        </label>
        <label>
          Longitude (east+)
          <input
            type="number"
            step="any"
            value={value.longitude}
            onChange={field("longitude", (v) => Number(v))}
          />
        </label>
        <label>
          Place name
          <input type="text" value={value.place_name} onChange={field("place_name", (v) => v)} />
        </label>
        <label>
          Name (optional)
          <input type="text" value={value.name} onChange={field("name", (v) => v)} />
        </label>
        <label>
          Time precision
          <select value={value.time_precision} onChange={field("time_precision", (v) => v)}>
            {["second", "minute", "fiveminute", "quarterhour", "hour", "unknown"].map((o) => (
              <option key={o} value={o}>
                {o}
              </option>
            ))}
          </select>
        </label>
        <label>
          Time source
          <select value={value.time_source} onChange={field("time_source", (v) => v)}>
            {["certificate", "hospital", "family", "memory", "rectified", "unknown"].map((o) => (
              <option key={o} value={o}>
                {o}
              </option>
            ))}
          </select>
        </label>
        <label>
          Sex
          <select value={value.sex} onChange={field("sex", (v) => v)}>
            {["male", "female", "unknown"].map((o) => (
              <option key={o} value={o}>
                {o}
              </option>
            ))}
          </select>
        </label>
        <label>
          Ayanamsa
          <input type="text" value={value.ayanamsa} onChange={field("ayanamsa", (v) => v)} />
        </label>
        <label>
          House system
          <input
            type="text"
            value={value.house_system}
            onChange={field("house_system", (v) => v)}
          />
        </label>
      </div>

      {touched && missing.length > 0 && (
        <p className="validation-error" role="alert">
          Required: {missing.join(", ")}
        </p>
      )}
      {touched && (!latValid || !lonValid) && (
        <p className="validation-error" role="alert">
          Latitude must be within -90..90 and longitude within -180..180.
        </p>
      )}

      <div className="form-actions">
        <button type="submit" disabled={submitting}>
          {submitting ? "Running consultation…" : "Run Consultation"}
        </button>
        <button
          type="button"
          onClick={() => onChange(DEFAULT_BIRTH_INPUT)}
          disabled={submitting}
        >
          Reset
        </button>
      </div>
    </form>
  );
}
