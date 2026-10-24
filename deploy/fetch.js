/* Build step: pull the pre-built static site (single self-contained HTML) into public/ */
const { execSync } = require('child_process');
const fs = require('fs');
const url = process.env.SITE_TGZ_URL;
if (!url) { console.error('SITE_TGZ_URL missing'); process.exit(1); }
execSync(`curl -fsSL --retry 3 -o site.tgz "${url}"`, { stdio: 'inherit' });
fs.mkdirSync('public', { recursive: true });
execSync('tar xzf site.tgz -C public && ls -l public', { stdio: 'inherit' });
