import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'We do not hold this record' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/We do not hold this record/);
  });

  test.describe("'Exit this form' and 'Back' links", () => {
    test("clicking the 'Exit this form' button takes the user to 'Are you sure you want to cancel?'", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Exit this form/i }).click();
      await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
    });

    test("clicking the 'Back' link on 'Are you sure you want to cancel? page brings the user back'", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Exit this form/i }).click();
      await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(
        Paths.WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS,
      );
    });

    test("clicking the 'No' link on 'Are you sure you want to cancel? page brings the user back'", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Exit this form/i }).click();
      await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
      // Falling back to a CSS selector here because there are multiple elements with the same role and name
      // I've tried to ensure it's not brittle
      await page.locator("form#cancel-request a").click();
      await expect(page).toHaveURL(
        Paths.WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS,
      );
    });
  });
});
