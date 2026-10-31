module.exports = {
  ci: {
    collect: {
      numberOfRuns: 3,
      startServerCommand: process.env.LHCI_START_SERVER_COMMAND || undefined,
      url: [process.env.LHCI_URL || 'http://localhost:3000/'],
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.90 }],
        'categories:accessibility': ['error', { minScore: 0.95 }],
        'categories:best-practices': ['error', { minScore: 0.90 }],
        'categories:seo': ['error', { minScore: 0.90 }],
        'first-contentful-paint': ['error', { maxNumericValue: 1800 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
      },
    },
    upload: {
      // Secure local filesystem output — never upload private client reports to public temporary storage
      target: 'filesystem',
      outputDir: './reports/lighthouse',
    },
  },
};
