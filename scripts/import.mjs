// Imports the HackEAC region CSVs into data/tanzania.csv: names cleaned, duplicates dropped, one code per ward.
// Usage: node scripts/import.mjs <path to tanzania-locations-db/location-files>

import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

import { parse, stringify } from "./csv.mjs";
import { clean } from "./names.mjs";

const dir = process.argv[2];
if (!dir) throw new Error("pass the folder holding the region CSV files");

const HEADER = ["region", "region_code", "district", "district_code", "ward", "ward_code", "street", "place"];
const rows = new Map();
const wardCode = new Map();

for (const file of readdirSync(dir).filter((f) => f.endsWith(".csv")).sort()) {
  const [, ...lines] = parse(readFileSync(join(dir, file), "utf8").replace(/^﻿/, ""));
  for (const cols of lines) {
    const [region, rc, district, dc, ward, wc, street, place] = cols.map((c) => (c ?? "").replace(/\s+/g, " ").trim());
    if (!region || !district || !ward) continue;
    const row = [clean(region), rc, clean(district), dc, clean(ward), wc, clean(street), clean(place)];
    const wardKey = row.slice(0, 5).join("|");
    if (!wardCode.has(wardKey) || wc < wardCode.get(wardKey)) wardCode.set(wardKey, wc);
    rows.set(row.join("|"), row);
  }
}

const out = new Map();
for (const row of rows.values()) {
  row[5] = wardCode.get(row.slice(0, 5).join("|"));
  out.set(row.join("|"), row);
}

const sorted = [...out.values()].sort((a, b) => a.join("|").localeCompare(b.join("|")));
writeFileSync("data/tanzania.csv", stringify([HEADER, ...sorted]));
console.log(`wrote ${sorted.length} rows to data/tanzania.csv`);
