// Builds json/ from data/: an index of every region and its districts, and one file per region down to places.
// Usage: node scripts/build.mjs

import { mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";

import { parse } from "./csv.mjs";
import { slug } from "./names.mjs";

const read = (file) => {
  const [header, ...rows] = parse(readFileSync(file, "utf8"));
  return rows.map((r) => Object.fromEntries(header.map((h, i) => [h, (r[i] ?? "").trim()])));
};

const child = (list, name, make) => {
  let found = list.find((x) => x.name === name);
  if (!found) list.push((found = { name, ...make() }));
  return found;
};

const regions = read("data/regions.csv").map((r) => ({ name: r.region, slug: slug(r.region), code: r.region_code, zone: r.zone, districts: [] }));

for (const row of read("data/tanzania.csv")) {
  const region = regions.find((r) => r.name === row.region);
  if (!region) throw new Error(`"${row.region}" is not in data/regions.csv`);
  const district = child(region.districts, row.district, () => ({ code: row.district_code, wards: [] }));
  const ward = child(district.wards, row.ward, () => ({ code: row.ward_code, streets: [] }));
  if (!row.street) continue;
  const street = child(ward.streets, row.street, () => ({ places: [] }));
  if (row.place && !street.places.includes(row.place)) street.places.push(row.place);
}

const byName = (a, b) => a.name.localeCompare(b.name);
rmSync("json", { recursive: true, force: true });
mkdirSync("json/regions", { recursive: true });

for (const region of regions.sort(byName)) {
  for (const d of region.districts.sort(byName)) {
    for (const w of d.wards.sort(byName)) {
      for (const s of w.streets.sort(byName)) s.places.sort((a, b) => a.localeCompare(b));
    }
  }
  writeFileSync(`json/regions/${region.slug}.json`, JSON.stringify(region) + "\n");
}

const index = regions.map(({ districts, ...r }) => ({ ...r, districts: districts.map(({ name, code }) => ({ name, code })) }));
writeFileSync("json/index.json", JSON.stringify(index) + "\n");

const count = (pick) => regions.flatMap(pick).length;
console.log(`${regions.length} regions, ${count((r) => r.districts)} districts, ${count((r) => r.districts.flatMap((d) => d.wards))} wards`);
