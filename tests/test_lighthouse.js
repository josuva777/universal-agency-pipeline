/**
 * Local Developer Lighthouse Audit Script
 * Validates performance, accessibility, best-practices, and SEO scores against production thresholds.
 */
const { execSync } = require('child_process');

const THRESHOLDS = {
  performance: 0.90,
  accessibility: 0.95,
  bestPractices: 0.90,
  seo: 0.90,
};

function runLocalAudit() {
  console.log('[*] Running Lighthouse CI audit against local server...');
  try {
    execSync('npx @lhci/cli autorun --config=./lighthouserc.js', { stdio: 'inherit' });
    console.log('[SUCCESS] All Lighthouse thresholds passed (Perf >= 90, A11y >= 95)!');
  } catch (error) {
    console.error('[!] Lighthouse assertions failed. Review report above.');
    process.exit(1);
  }
}

if (require.main === module) {
  runLocalAudit();
}

module.exports = { THRESHOLDS, runLocalAudit };

