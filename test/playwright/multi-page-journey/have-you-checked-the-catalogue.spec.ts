import { test, expect } from "@playwright/test";

test.describe("'Have you checked the catalogue?' form", () => {
  const JOURNEY_START_PAGE_URL = "/request-a-service-record/start/";
  const HAVE_YOU_CHECKED_THE_CATALOGUE =
    "/request-a-service-record/have-you-checked-the-catalogue/";

  test.beforeEach(async ({ page }) => {
    await page.goto(JOURNEY_START_PAGE_URL);
    await page.goto(HAVE_YOU_CHECKED_THE_CATALOGUE);
  });

  test("Has the right heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /Have you checked if this record is available in our catalogue\?/,
    );
  });

  test("clicking 'Next' without having made a selection keeps the user on the page and shows a validation error", async ({
    page,
  }) => {
    await page.getByRole("button", { name: /Next/i }).click();
    await expect(page).toHaveURL(HAVE_YOU_CHECKED_THE_CATALOGUE);
    await expect(page.locator(".tna-form__error-message")).toHaveText(
      /Choosing an option is required/,
    );
  });
});
