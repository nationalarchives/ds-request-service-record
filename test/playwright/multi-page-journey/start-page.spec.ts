import { test, expect } from "@playwright/test";

test.describe("application start page", () => {
  enum Urls {
    START_PAGE = "/request-a-service-record/start/",
    HAVE_YOU_CHECKED_THE_CATALOGUE = "/request-a-service-record/have-you-checked-the-catalogue/",
  }

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.START_PAGE);
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
    await expect(page).toHaveURL(Urls.HAVE_YOU_CHECKED_THE_CATALOGUE);
    await expect(page.locator("h1")).toHaveText(
      /Have you checked if this record is available in our catalogue\?/,
    );
  });

  test("clicking 'Back' from 'Have you checked the catalogue?' brings the user back to the start page", async ({
    page,
  }) => {
    await page.getByRole("button", { name: /Start now/i }).click();
    await expect(page).toHaveURL(Urls.HAVE_YOU_CHECKED_THE_CATALOGUE);
    await page.getByRole("link", { name: "Back" }).click();
    await expect(page).toHaveURL(Urls.START_PAGE);
  });
});
