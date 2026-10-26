# mahali

Every place in Tanzania, from region down to street and village, in one tidy list.

*Mahali* is Swahili for "place". Use it for address dropdowns, search and checks, in any language.

| Level | Count |
| --- | --- |
| Regions | 31 (26 mainland, 5 Zanzibar) |
| Districts | 158 |
| Wards | 3,959 |
| Streets | 16,692 |
| Places (villages, hamlets) | 64,000+ |

Zanzibar's five regions are listed; their districts, wards and shehia are not in yet. Help add them.

## Files

| File | What it holds |
| --- | --- |
| `data/regions.csv` | All 31 regions: name, postcode prefix, zone |
| `data/tanzania.csv` | One row per place: region, district, ward, street, place, with postcodes. The source of truth |
| `json/index.json` | Every region with its districts. Small, load it first |
| `json/regions/<region>.json` | One region down to places, e.g. `json/regions/dar-es-salaam.json` |

Codes are postcodes: `23` is Arusha, `231` Arusha CBD, `23101` Sekei ward.

```json
{ "name": "Arusha", "slug": "arusha", "code": "23", "zone": "mainland",
  "districts": [{ "name": "Arusha CBD", "code": "231",
    "wards": [{ "name": "Sekei", "code": "23101",
      "streets": [{ "name": "Sanawari", "places": [] }] }] }] }
```

## Use it

Straight from GitHub:

```
https://raw.githubusercontent.com/isonlycoolie/mahali/main/json/index.json
https://raw.githubusercontent.com/isonlycoolie/mahali/main/json/regions/mwanza.json
```

Or as a package:

```sh
npm install github:isonlycoolie/mahali
```

```js
import regions from "mahali/json/index.json" with { type: "json" };
```

Load `index.json` for the region and district pickers, then fetch one region file when someone picks a region.

## Add or fix a place

1. Edit `data/tanzania.csv` (or `data/regions.csv` for a region).
2. Run `node scripts/build.mjs` to rebuild `json/`. Node 20 or newer, nothing to install.
3. Open a pull request with both changes.

Names are written the way people write them: `Dar es Salaam`, `Chang'ombe`, `Mtaa wa AICC`.

## Where it comes from

The mainland list started from the national postcode listing as gathered in
[HackEAC/tanzania-locations-db](https://github.com/HackEAC/tanzania-locations-db), then cleaned:
names in normal case, stray quotes removed, duplicate rows dropped and one code per ward.
`node scripts/import.mjs <folder of region CSVs>` repeats that import.
