---
name: accessibility-audit
description: >-
  WCAG 2.2 AA accessibility compliance, automated axe-core scans, screen reader testing patterns,
  keyboard navigation, color contrast verification (4.5:1), focus traps, and touch targets (24x24px).
  Trigger phrases: "accessibility", "a11y", "wcag", "axe-core", "screen reader", "keyboard navigation",
  "color contrast", "touch target", "accessible ui".
---

# WCAG 2.2 AA Accessibility Engineering Standard

This skill establishes full **WCAG 2.2 AA compliance** across all web and mobile deliverables. Accessibility is not an afterthought; it is an intrinsic quality attribute that eliminates legal liability, guarantees universal access, and improves SEO.

---

## 1. The WCAG 2.2 Core Mandates

| Criterion | Rule | Engineering Requirement |
| :--- | :--- | :--- |
| **2.4.11** | Focus Not Obscured | Elements receiving keyboard focus must never be hidden behind sticky headers or fixed footers. |
| **2.5.7** | Dragging Movements | All drag operations (sliders, reordering) must have single-pointer click/touch alternatives. |
| **2.5.8** | Target Size (Minimum) | Interactive elements MUST be at least **24×24 CSS pixels** or have adequate surrounding spacing. |
| **3.3.8** | Accessible Authentication | Login flows must not force complex cognitive memory puzzles (transcription of distorted text). |
| **1.4.3** | Contrast (Minimum) | Contrast ratio between text and background MUST be at least **4.5:1** for regular text, **3:1** for large text (≥18pt). |
| **4.1.2** | Name, Role, Value | All custom interactive controls (toggles, accordions, tabs) must expose appropriate ARIA attributes. |

---

## 2. Automated Testing with Playwright & Axe-Core

Every page and state must be validated using `@axe-core/playwright`. No PR may be merged with critical or serious violations:

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('WCAG 2.2 AA Automated Accessibility Suite', () => {
  test('Landing page zero violations', async ({ page }) => {
    await page.goto('/');
    
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('Interactive dialog modal focus trap & escape key', async ({ page }) => {
    await page.goto('/');
    await page.click('button[aria-haspopup="dialog"]');
    
    // Modal must be mounted with role="dialog" and aria-modal="true"
    const modal = page.locator('div[role="dialog"]');
    await expect(modal).toBeVisible();

    // Verify axe-core inside open modal
    const modalA11y = await new AxeBuilder({ page })
      .include('div[role="dialog"]')
      .analyze();
    expect(modalA11y.violations).toEqual([]);

    // Press Escape to dismiss
    await page.keyboard.press('Escape');
    await expect(modal).toBeHidden();
  });
});
```

---

## 3. Keyboard Navigation & Focus Management

1. **Logical Tab Order**:
   - Tab navigates strictly top-to-bottom, left-to-right.
   - Never use `tabindex` greater than `0`. Use `tabindex="0"` to make elements focusable; use `tabindex="-1"` for programmatic focus.
2. **Visible Focus Rings**:
   - Never write `outline: none` without providing an enhanced `:focus-visible` ring.
   - Example Tailwind: `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950`.
3. **Skip Navigation Links**:
   - Include a hidden-until-focused skip link as the very first focusable element on every page:
   ```tsx
   <a
     href="#main-content"
     className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-emerald-500 focus:text-slate-950 focus:font-bold focus:rounded-lg"
   >
     Skip to main content
   </a>
   ```

---

## 4. Forms, Labels & Screen Reader Patterns

1. **Every Input Has an Explicit Label**:
   ```tsx
   // Correct (Programmatically Associated):
   <label htmlFor="work-email" className="block text-sm font-medium text-slate-300">
     Work Email Address
   </label>
   <input
     id="work-email"
     type="email"
     required
     aria-describedby="email-hint"
     className="..."
   />
   <p id="email-hint" className="text-xs text-slate-500">
     We will dispatch your 6-digit cryptographic verification code here.
   </p>
   ```

2. **Live Announcements (`aria-live`)**:
   - Dynamic alerts (e.g., OTP countdown timer, quota changes, security block notices) must be wrapped in `aria-live="polite"` or `role="status"` so screen readers announce changes without interrupting the user:
   ```tsx
   <div role="status" aria-live="polite" className="sr-only">
     {statusMessage}
   </div>
   ```

3. **Internationalization & RTL Readiness**:
   - Use CSS logical properties instead of physical directions:
     - `margin-inline-start` instead of `margin-left`
     - `padding-inline-end` instead of `padding-right`
   - Ensure the root HTML tag reflects the active document language: `<html lang="en" dir="ltr">`.

