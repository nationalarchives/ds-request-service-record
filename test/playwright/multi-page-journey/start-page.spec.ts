import { test, expect } from "@playwright/test";

test.describe("application start page", () => {
  const JOURNEY_START_PAGE_URL = "/request-a-service-record/start/";
  const HAVE_YOU_CHECKED_THE_CATALOGUE =
    "/request-a-service-record/have-you-checked-the-catalogue/";

  test.beforeEach(async ({ page }) => {
    await page.goto(JOURNEY_START_PAGE_URL);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /Request a military service record/,
    );
  });

  test("clicking 'Start now' takes the user to the 'Have you checked the catalogue?' form", async ({
    page,
  }) => {
    await page.getByRole("button", { name: /Start now/i }).click();
    await expect(page).toHaveURL(HAVE_YOU_CHECKED_THE_CATALOGUE);
    await expect(page.locator("h1")).toHaveText(
      /Have you checked if this record is available in our catalogue\?/,
    );
  });
});
