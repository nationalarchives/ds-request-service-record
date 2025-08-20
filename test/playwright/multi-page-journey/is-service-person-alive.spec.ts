import { test, expect } from "@playwright/test";

test.describe("application start page", () => {
  const JOURNEY_START_PAGE_URL = "/request-a-service-record/start/";

  test.beforeEach(async ({ page }) => {
    await page.context().clearCookies();
    await page.goto(JOURNEY_START_PAGE_URL);
  });

  test("Has the right heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /Request a military service record/,
    );
  });

  test("clicking 'Start now' takes the user to the 'Is service person still alive?' form", async ({
    page,
  }) => {
    await page.getByRole("button", { name: /Start now/i }).click();
    await expect(page).toHaveURL(
      "/request-a-service-record/is-service-person-alive/",
    );
    await expect(page.locator("h1")).toHaveText(
      /Is this person still alive\?/,
    );
  });
});
