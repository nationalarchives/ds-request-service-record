import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'Before you start' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.BEFORE_YOU_START);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/Before you start/);
  });

  test.describe("clicking 'Start now'", () => {
    test("without selecting an option shows an error message", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Start now/i }).click();
      await expect(page.locator(".tna-error-summary__list")).toHaveText(
        /You must confirm you have the mandatory information before starting/,
      );
    });

    test("after checking the checkbox, takes user to the next page", async ({
      page,
    }) => {
      await page
        .getByLabel(/I have all the mandatory information/)
        .check({ force: true });
      await page.getByRole("button", { name: /Start now/i }).click();
      await expect(page).toHaveURL(Paths.YOU_MAY_WANT_TO_CHECK_ANCESTRY);
    });
  });

  test.describe("the 'Exit this form' link", () => {
    test("takes the user to the 'Are you sure you want to cancel?' page", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Exit this form" }).click();
      await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
    });
  });
});
