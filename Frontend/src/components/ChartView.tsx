import type { ChartBundle } from "../types";

interface Props {
  chart: ChartBundle;
}

/** §21: a table of houses 1-12 with their occupants -- a view of the engine's
 * own ChartBundle, not a second chart-drawing or chart-calculation engine. */
export function ChartView({ chart }: Props) {
  const byHouse = new Map<number, string[]>();
  for (let h = 1; h <= 12; h++) byHouse.set(h, []);
  for (const body of Object.values(chart.bodies)) {
    byHouse.get(body.house)?.push(body.body);
  }

  return (
    <section>
      <h2>Chart</h2>
      <p>
        Ascendant: <strong>{chart.ascendant_sign}</strong> ({chart.ascendant.toFixed(4)}°) ·
        Midheaven: {chart.midheaven.toFixed(4)}° · Houses: {chart.houses.system}
      </p>

      <table className="chart-table">
        <thead>
          <tr>
            <th>House</th>
            <th>Sign</th>
            <th>Occupants</th>
          </tr>
        </thead>
        <tbody>
          {chart.houses.signs.map((sign, i) => {
            const house = i + 1;
            return (
              <tr key={house} className={house === 1 ? "lagna-row" : ""}>
                <td>{house}</td>
                <td>{sign}</td>
                <td>{(byHouse.get(house) ?? []).join(", ") || "—"}</td>
              </tr>
            );
          })}
        </tbody>
      </table>

      <h3>Graha placements</h3>
      <table className="chart-table">
        <thead>
          <tr>
            <th>Graha</th>
            <th>Sign</th>
            <th>Degree in sign</th>
            <th>House</th>
            <th>Nakshatra</th>
            <th>Pada</th>
            <th>Retrograde</th>
          </tr>
        </thead>
        <tbody>
          {Object.values(chart.bodies).map((b) => (
            <tr key={b.body}>
              <td>{b.body}</td>
              <td>{b.sign}</td>
              <td>{b.deg_in_sign.toFixed(2)}°</td>
              <td>{b.house}</td>
              <td>{b.nakshatra}</td>
              <td>{b.pada}</td>
              <td>{b.retrograde ? "R" : ""}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
