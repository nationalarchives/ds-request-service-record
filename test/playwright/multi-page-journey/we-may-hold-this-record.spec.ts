import { test, expect } from "@playwright/test";

test.describe("the 'We may hold this record' form", () => {
  const basePath = "/request-a-service-record";

  enum Urls {
    JOURNEY_START_PAGE = `${basePath}/start/`,
    WE_MAY_HOLD_THIS_RECORD = `${basePath}/we-may-hold-this-record/`,
    WHAT_WAS_THEIR_DATE_OF_BIRTH = `${basePath}/what-was-their-date-of-birth/`,
  }

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.JOURNEY_START_PAGE); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Urls.WE_MAY_HOLD_THIS_RECORD);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/We may hold this record/);
  });

  test.describe("when submitted", () => {
    test("the user is taken to the 'What was their date of birth?' page", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(Urls.WHAT_WAS_THEIR_DATE_OF_BIRTH);
      await expect(page.locator("h1")).toHaveText(
        /What was their date of birth?/,
      );
    });
  });
});
