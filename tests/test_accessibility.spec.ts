import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('WCAG 2.2 AA Compliance Gate', () => {
  test('Landing page has 0 accessibility violations', async ({ page }) => {
    await page.goto('/');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();

    if (accessibilityScanResults.violations.length > 0) {
      console.error(
        'Accessibility Violations Found:',
        JSON.stringify(accessibilityScanResults.violations, null, 2)
      );
    }

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('All interactive buttons meet minimum 24x24 touch target', async ({ page }) => {
    await page.goto('/');
    const buttons = await page.locator('button:visible').all();

    for (const btn of buttons) {
      const box = await btn.boundingBox();
      if (box) {
        expect(box.width).toBeGreaterThanOrEqual(24);
        expect(box.height).toBeGreaterThanOrEqual(24);
      }
    }
  });
});

