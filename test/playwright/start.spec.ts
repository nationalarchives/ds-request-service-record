import { test, expect } from "@playwright/test";
import acceptAllCookies from "./lib/accept-all-cookies.ts";
import validateHtml from "./lib/validate-html.ts";
import checkAccessibility from "./lib/check-accessibility.ts";

acceptAllCookies();

test("development landing page", async ({ page }) => {
  await page.goto("/request-a-service-record/");
  await expect(page.locator("h1")).toHaveText(/Request a Service Record/);
  await validateHtml(page);
  await checkAccessibility(page);
});

test("all fields form", async ({ page }) => {
  await page.goto("/request-a-service-record/all-fields-in-one-form/");
  await expect(page.locator("h1")).toHaveText(/Request a Service Record/);
  await validateHtml(page);
  await checkAccessibility(page);
});
