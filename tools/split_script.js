/* Split one story's narration into TTS sized chunks -> audio/parts/<id>/partN.txt
   usage: node tools/split_script.js bhangarh [maxChars=1350]  |  node tools/split_script.js --all */
const fs = require('fs'), path = require('path');
const scripts = JSON.parse(fs.readFileSync(__dirname + '/../audio/scripts.json', 'utf8'));
function chunks(text, max) {
  const sents = text.replace(/\n+/g, ' ').match(/[^.!?…]+[.!?…]+["”’]?|\S[^.!?…]*$/g) || [text];
  const out = []; let buf = '';
  for (const s of sents) {
    if ((buf + s).length > max) { if (buf.trim()) out.push(buf.trim()); buf = ''; }
    buf += s + ' ';
  }
  if (buf.trim()) out.push(buf.trim());
  return out;
}
const args = process.argv.slice(2);
const max = Number(args.find(a => /^\d+$/.test(a))) || 1350;
const ids = args[0] === '--all' ? Object.keys(scripts) : args.filter(a => !/^\d+$/.test(a));
let total = 0;
ids.forEach(id => {
  if (!scripts[id]) return console.log('skip', id);
  const cs = chunks(scripts[id].text, max);
  const dir = path.join(__dirname, '../audio/parts', id);
  fs.mkdirSync(dir, { recursive: true });
  cs.forEach((c, i) => fs.writeFileSync(path.join(dir, `part${i + 1}.txt`), c));
  total += cs.length;
  console.log(id, cs.length, 'parts');
});
console.log('total clips needed:', total);
