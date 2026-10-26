<p align="center">
  <img src="brand/png/banner-1600.png" alt="mahali: every place in Tanzania, from region down to street" width="100%">
</p>

<p align="center">
  <strong>Every place in Tanzania, from region down to street.</strong><br>
  31 regions · 158 districts · 3,959 wards · 16,692 streets · 64,000+ villages and hamlets
</p>

---

**mahali** (Swahili for *place*) is a clean, open list of Tanzania's places, ready for address forms, search and data checks. It ships as plain CSV and JSON, so it works in any language, on any platform, with nothing to install.

Built for the moment a person fills in an address: pick a region, then a district, a ward and a street, each one a short searchable list. No more "Dar es salaam", "DSM" and "Dar-es-Salaam" in the same database.

## Contents

- [Quick start](#quick-start)
- [What's inside](#whats-inside)
- [Data shape](#data-shape)
- [Building an address picker](#building-an-address-picker)
- [Contributing](#contributing)
- [Brand](#brand)

## Quick start

Load the index straight from GitHub. It holds every region with its districts and is small enough to load on first paint.

```js
const base = "https://raw.githubusercontent.com/isonlycoolie/mahali/main/json";

const regions = await fetch(`${base}/index.json`).then((r) => r.json());
const mwanza = await fetch(`${base}/regions/mwanza.json`).then((r) => r.json());
```

Or install it as a package and import the files directly:

```sh
npm install github:isonlycoolie/mahali
```

```js
import regions from "mahali/json/index.json" with { type: "json" };
import dar from "mahali/json/regions/dar-es-salaam.json" with { type: "json" };
```

## What's inside

- **`data/regions.csv`** lists all 31 regions with their postcode prefix and zone (mainland or Zanzibar).
- **`data/tanzania.csv`** holds one row per place: region, district, ward, street and village, each with its postcode. This is the source of truth; everything else is generated from it.
- **`json/index.json`** has every region and its districts, about 8 KB.
- **`json/regions/<region>.json`** has one region in full, down to villages, for example `json/regions/arusha.json`.

Names are written the way Tanzanians write them: `Dar es Salaam`, `Chang'ombe`, `Mtaa wa AICC`. Codes are postcodes, so `23` is Arusha, `231` is Arusha CBD and `23101` is Sekei ward.

Zanzibar's five regions are listed. Their districts, wards and shehia are the next addition, and contributions are very welcome.

