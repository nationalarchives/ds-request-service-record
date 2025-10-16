import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("request submitted", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.REQUEST_SUBMITTED);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/Request submitted/);
  });

  test("includes the reference number", async ({ page }) => {
    await expect(page.locator("#reference-number")).toBeAttached();
  });

  test("the reference number is in the correct format", async ({ page }) => {
    // For the time-being, we're just testing that it's a 6-digit number.
    // We'll need to update the RegEx when we know the actual format
    await expect(page.locator("#reference-number")).toHaveText(/^\d{6}$/);
  });
});
