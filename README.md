<p align="center">
  <img src="brand/png/banner-1600.png" alt="mahali: Tanzania regions, districts, wards and streets list with postcodes" width="100%">
</p>

<p align="center">
  <img src="brand/svg/mark-on-dark.svg" width="40" alt="mahali">
</p>

<p align="center">
  <strong>Every place in Tanzania, from region down to street.</strong><br>
  31 regions · 158 districts · 3,959 wards · 16,692 streets · 64,000+ villages and hamlets
</p>

---

**mahali** (Swahili for *place*) is a clean, open list of every region, district, ward, street and village in Tanzania, with postcodes. Use it for address forms, dropdowns, autocomplete, search and data checks. It ships as plain CSV and JSON, so it works in any language, on any platform, with nothing to install.

*Mikoa, wilaya, kata, mitaa na vijiji vyote vya Tanzania, pamoja na postikodi, tayari kwa fomu za anwani.*

Built for the moment a person fills in an address: pick a region, then a district, a ward and a street, each one a short searchable list. No more "Dar es salaam", "DSM" and "Dar-es-Salaam" in the same database.

## Contents

- [Quick start](#quick-start)
- [What's inside](#whats-inside)
- [Data shape](#data-shape)
- [Building an address picker](#building-an-address-picker)
- [Contributing](#contributing)

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

## Data shape

Each region file nests districts, wards, streets and places, sorted by name:

```json
{
  "name": "Arusha",
  "slug": "arusha",
  "code": "23",
  "zone": "mainland",
  "districts": [
    {
      "name": "Arusha CBD",
      "code": "231",
      "wards": [
        {
          "name": "Sekei",
          "code": "23101",
          "streets": [{ "name": "Sanawari", "places": [] }]
        }
      ]
    }
  ]
}
```

## Building an address picker

1. Load `json/index.json` once and fill the region list.
2. When someone picks a region, fetch that region's file and fill the district list.
3. Fill wards from the chosen district and streets from the chosen ward.
4. Put a search box at the top of every list, and let people type a place the list does not have yet, such as a new street or a Zanzibar ward.
5. When a choice changes, clear the levels below it, so a ward never sits under the wrong district.

The largest region file is under 100 KB, so a phone on a slow network loads it in a moment.

## Contributing

Corrections and additions are welcome, from a misspelt street to a whole region.

1. Edit `data/tanzania.csv`, or `data/regions.csv` for a region.
2. Rebuild the JSON with `node scripts/build.mjs`. It needs Node 20 or newer and nothing else.
3. Open a pull request with both changes and a line on where the information comes from.

Keep one row per place, use the local spelling, and leave a column empty rather than guessing.
