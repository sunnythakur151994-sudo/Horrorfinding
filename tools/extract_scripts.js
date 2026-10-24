/* Extract clean narration text for every story -> audio/scripts.json
   usage: node tools/extract_scripts.js
   (reads the built index.html so text is exactly what the page shows) */
const fs = require('fs');
const html = fs.readFileSync(__dirname + '/../index.html', 'utf8');
const js = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const noImg = js.replace(/const IMG = \{[\s\S]*?\n\};/, 'const IMG={};');
const STORIES = new Function(noImg + '; return STORIES;')();
const out = {};
STORIES.forEach(s => {
  const text = (s.body || '')
    .replace(/<figcaption[\s\S]*?<\/figcaption>/g, ' ')
    .replace(/<h3>/g, '\n\n').replace(/<\/h3>/g, '.\n\n')
    .replace(/<\/p>/g, '\n\n')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&quot;/g, '"')
    .replace(/[ \t]+/g, ' ').replace(/\n{3,}/g, '\n\n').trim();
  out[s.id] = { title: s.title, cat: s.cat, words: s.words, text };
});
fs.mkdirSync(__dirname + '/../audio', { recursive: true });
fs.writeFileSync(__dirname + '/../audio/scripts.json', JSON.stringify(out, null, 1));
console.log('wrote audio/scripts.json —', Object.keys(out).length, 'stories');
