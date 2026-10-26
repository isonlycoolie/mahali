// Turns the shouting, quote-scattered source names into the way people write them: "MTAA WA AICC" -> "Mtaa wa AICC".

const KEEP_UPPER = new Set(["CBD", "AICC", "JKT", "KKKT", "NHC", "TPDC", "TRC", "TAZARA", "TANESCO", "NSSF", "NMB", "CRDB", "SDA", "RC", "DC"]);
const SMALL = new Set(["wa", "ya", "la", "za", "cha", "vya", "kwa", "na", "es", "el"]);
const ROMAN = /^(I|II|III|IV|V|VI|VII|VIII|IX|X)$/;
const FIXED = new Map([["dar-es-salaam", "Dar es Salaam"], ["dar es salaam", "Dar es Salaam"]]);

function word(w, first) {
  if (!w) return w;
  const up = w.toUpperCase();
  if (KEEP_UPPER.has(up) || ROMAN.test(up) || /\d/.test(w) || w.length === 1) return up;
  const low = w.toLowerCase();
  if (!first && SMALL.has(low)) return low;
  return low.replace(/(^|-)([a-z])/g, (_, sep, ch) => sep + ch.toUpperCase());
}

// Swahili writes ng' as one sound (Chang'ombe, Hanang'); the source sometimes typed it as an accent (Kingúna).
// Any other stray quote is noise.
function keepApostrophe(str, i) {
  const letter = (c) => /\p{L}/u.test(c ?? "");
  return (letter(str[i - 1]) && letter(str[i + 1])) || /ng$/i.test(str.slice(0, i));
}

export function clean(raw) {
  let s = raw
    .replace(/(ng)([áéíóú])/gi, (_, ng, v) => `${ng}'${v.normalize("NFD")[0]}`)
    .replace(/[“”‘’`"]/g, " ")
    .replace(/[^\p{L}\p{N}\s'\-/.,()&]/gu, " ")
    .replace(/'/g, (_, i, str) => (keepApostrophe(str, i) ? "'" : " "))
    .replace(/\s*\/\s*/g, " / ")
    .replace(/\s+/g, " ")
    .trim();
  const fixed = FIXED.get(s.toLowerCase());
  if (fixed) return fixed;
  s = s.split(" ").map((w, i) => word(w, i === 0)).join(" ");
  return s.replace(/\b(Fr|St|Mt)\.(?=\S)/g, "$1. ");
}

export const slug = (name) => name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
