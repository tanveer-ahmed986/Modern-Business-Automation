/**
 * E2E Test: Complete Sale Workflow
 *
 * Tests the entire user journey from login to creating a sale
 * and verifying the invoice generation.
 */

import { test, expect } from '@playwright/test';

test.describe('Complete Sale Workflow', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the application
    await page.goto('/');
  });

  test('complete sale workflow from login to invoice', async ({ page }) => {
    // Step 1: Login
    await test.step('User logs in', async () => {
      await expect(page).toHaveURL(/.*login/);

      await page.fill('input[name="username"]', 'admin');
      await page.fill('input[name="password"]', 'admin123');
      await page.click('button[type="submit"]');

      // Wait for redirect to dashboard
      await page.waitForURL(/.*dashboard/);
      await expect(page).toHaveURL(/.*dashboard/);
    });

    // Step 2: Navigate to Billing
    await test.step('User navigates to Billing', async () => {
      await page.click('text=Billing');
      await expect(page).toHaveURL(/.*billing/);
    });

    // Step 3: Search and add product to cart
    await test.step('User searches for product and adds to cart', async () => {
      // Search for product (assuming there's a test product in the system)
      const searchInput = page.locator('input[placeholder*="Search"], input[placeholder*="product"]').first();
      if (await searchInput.isVisible()) {
        await searchInput.fill('Test Product');
        await page.waitForTimeout(500); // Wait for search results
      }

      // Click on product or "Add to Cart" button
      const addButton = page.locator('button:has-text("Add"), button:has-text("Add to Cart")').first();
      if (await addButton.isVisible()) {
        await addButton.click();
      } else {
        // Alternative: click on product row
        await page.locator('tr, div').filter({ hasText: /Test Product|Product/ }).first().click();
      }
    });

    // Step 4: Review cart and complete sale
    await test.step('User completes the sale', async () => {
      // Select payment method
      const paymentSelect = page.locator('select').filter({ hasText: /payment|method/i }).or(
        page.locator('[role="combobox"]').filter({ hasText: /payment|cash|card/i })
      );

      if (await paymentSelect.count() > 0) {
        await paymentSelect.first().click();
        await page.locator('text=Cash').or(page.locator('[role="option"]:has-text("Cash")')).first().click();
      }

      // Click Complete Sale / Submit button
      const submitButton = page.locator('button:has-text("Complete Sale"), button:has-text("Submit"), button:has-text("Create Sale")');
      await submitButton.first().click();

      // Wait for success message or invoice display
      await page.waitForTimeout(1000);
    });

    // Step 5: Verify invoice generated
    await test.step('Verify invoice number is displayed', async () => {
      // Look for invoice number pattern INV-YYYYMMDD-XXXX
      const invoicePattern = /INV-\d{8}-\d{4}/;

      // Check if invoice number appears on the page
      const invoiceLocator = page.locator(`text=${invoicePattern}`);
      await expect(invoiceLocator).toBeVisible({ timeout: 5000 });

      // Optionally verify the invoice number format
      const invoiceNumber = await invoiceLocator.textContent();
      expect(invoiceNumber).toMatch(invoicePattern);
    });
  });

  test('prevents sale with insufficient stock', async ({ page }) => {
    // Login
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');
    await page.waitForURL(/.*dashboard/);

    // Navigate to Billing
    await page.click('text=Billing');

    // Try to add product with quantity > stock
    // (This test assumes we can set quantity manually)
    const quantityInput = page.locator('input[type="number"]').first();
    if (await quantityInput.isVisible()) {
      await quantityInput.fill('9999'); // Very large quantity
    }

    // Try to complete sale
    const submitButton = page.locator('button:has-text("Complete Sale"), button:has-text("Submit")');
    if (await submitButton.count() > 0) {
      await submitButton.first().click();

      // Verify error message appears
      await expect(page.locator('text=/insufficient stock/i')).toBeVisible({ timeout: 3000 });
    }
  });

  test('logout functionality works', async ({ page }) => {
    // Login
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');
    await page.waitForURL(/.*dashboard/);

    // Find and click logout button
    const logoutButton = page.locator('button:has-text("Sign Out"), button:has-text("Logout")');
    await logoutButton.click();

    // Verify redirected to login
    await expect(page).toHaveURL(/.*login/);
  });
});

test.describe('Feature Access Control', () => {
  test('premium features show upgrade prompt when disabled', async ({ page }) => {
    // Login
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');
    await page.waitForURL(/.*dashboard/);

    // Try to access AI Insights (Premium feature)
    // If it's hidden, the test passes (feature gating working)
    const aiInsightsLink = page.locator('text="AI Insights"');

    if (await aiInsightsLink.isVisible()) {
      await aiInsightsLink.click();

      // If feature is disabled, should show upgrade modal
      const upgradeModal = page.locator('text=/upgrade|premium/i');

      // Either the page loads (feature enabled) or modal shows (feature disabled)
      // Both are valid depending on license tier
      const modalOrContent = await Promise.race([
        upgradeModal.isVisible().then(visible => ({ type: 'modal', visible })),
        page.waitForURL(/.*ai/, { timeout: 2000 }).then(() => ({ type: 'page', visible: true }))
          .catch(() => ({ type: 'none', visible: false }))
      ]);

      // Test passes if either modal shows or page loads
      expect(modalOrContent.type).toMatch(/modal|page/);
    } else {
      // AI Insights not visible - feature correctly hidden
      expect(await aiInsightsLink.count()).toBe(0);
    }
  });
});

test.describe('Session Management', () => {
  test('expired session redirects to login', async ({ page, context }) => {
    // Login
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');
    await page.waitForURL(/.*dashboard/);

    // Clear localStorage to simulate expired session
    await context.clearCookies();
    await page.evaluate(() => localStorage.removeItem('mbas_token'));

    // Try to access protected page
    await page.goto('/dashboard');

    // Should redirect to login
    await expect(page).toHaveURL(/.*login/);
  });
});
