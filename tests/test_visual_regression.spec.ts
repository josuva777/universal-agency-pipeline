import { test, expect } from '@playwright/test';

const VIEWPORTS = [
  { width: 375, height: 812, name: 'mobile-iphone-13' },
  { width: 1024, height: 768, name: 'tablet-ipad' },
  { width: 1440, height: 900, name: 'desktop-macbook' },
];

test.describe('Visual Regression Multi-Viewport Audit', () => {
  for (const vp of VIEWPORTS) {
    test(`Landing Page renders without visual diff @ ${vp.name}`, async ({ page }) => {
      await page.setViewportSize({ width: vp.width, height: vp.height });
      await page.goto('/');

      // Wait for font loading and animations to settle
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(500);

      await expect(page).toHaveScreenshot(`landing-${vp.name}.png`, {
        maxDiffPixelRatio: 0.02,
      });
    });
  }
});
