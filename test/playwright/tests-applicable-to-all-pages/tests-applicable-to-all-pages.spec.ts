import { test } from "@playwright/test";
import acceptAllCookies from "../lib/accept-all-cookies";
import validateHtml from "../lib/validate-html";
import checkAccessibility from "../lib/check-accessibility";
import {
  checkPageTypeMetaTag,
  checkContentGroupMetaTag,
} from "../lib/check-analytics-meta-tag";
import { Paths } from "../lib/constants";

acceptAllCookies();

test.describe("All pages pass automated tests", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
  });

  test.describe("HTML validation", () => {
    Object.keys(Paths).forEach((key) => {
      test(`${key} has valid HTML`, async ({ page }) => {
        await page.goto(Paths[key]);
        await validateHtml(page);
      });
    });
  });

  test.describe("Accessibility tests", () => {
    Object.keys(Paths).forEach((key) => {
      test(`${key} passes automated accessibility checks`, async ({ page }) => {
        await page.goto(Paths[key]);
        await checkAccessibility(page);
      });
    });
  });
  test.describe("Analytics meta tag tests", () => {
    Object.keys(Paths).forEach((key) => {
      test(`${key} has the page type and content group meta tags`, async ({
        page,
      }) => {
        await page.goto(Paths[key]);
        await checkPageTypeMetaTag(page);
        await checkContentGroupMetaTag(page);
      });
    });
  });
});
