import { test } from "@playwright/test";
import acceptAllCookies from "../lib/accept-all-cookies";
import validateHtml from "../lib/validate-html";
import checkAccessibility from "../lib/check-accessibility";
import { Paths } from "../lib/constants";

acceptAllCookies();

test.describe("All pages pass automated tests", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
  });

  Object.keys(Paths).forEach((key) => {
    test(`${key} has valid HTML`, async ({ page }) => {
      await page.goto(Paths[key]);
      await validateHtml(page);
      await checkAccessibility(page);
    });

    test(`${key} passes automated accessibility checks`, async ({ page }) => {
      await page.goto(Paths[key]);
      await validateHtml(page);
      await checkAccessibility(page);
    });
  });
});
