import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("choose your order type", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.REQUEST_SUBMITTED);
  });

  test.describe("when first rendered", () => {
    test("has the correct heading", async ({ page }) => {
      await expect(page.locator("h1")).toHaveText(/Request submitted/);
    });
  });
});
