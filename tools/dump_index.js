#!/usr/bin/env node
/* Dump story metadata from the built index.html into editorial/stories-index.json.
   Used by editorial/make_leonardo_prompts.py (one prompt per story).
   Usage: node tools/dump_index.js */
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const html = fs.readFileSync(path.join(ROOT, "index.html"), "utf8");
const script = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)][0][1];
const i = script.indexOf("/* ---- assemble");
const j = script.indexOf("})();", i) + 5;
const code = script.slice(0, i) + "\n" + script.slice(i, j) + "\nmodule.exports = {STORIES};";
const mod = { exports: {} };
new Function("module", "exports", code)(mod, mod.exports);
const rows = mod.exports.STORIES.map(s => ({
  id: s.id, cat: s.cat, no: s.no, title: s.title, card: s.card, zone: s.zone,
  regionLabel: s.regionLabel || s.zoneLabel || "", era: s.era || "", label: s.label || "",
  art: s.art || s.img || "", words: s.words || 0,
}));
const out = path.join(ROOT, "editorial", "stories-index.json");
fs.writeFileSync(out, JSON.stringify(rows, null, 1));
console.log("wrote", out, rows.length, "stories");
