import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'Before you start' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /Are you sure you want to cancel?/,
    );
  });

  test("clicking 'Yes' takes the user to 'You have cancelled your request'", async ({
    page,
  }) => {
    // Falling back to a CSS selector here because there are multiple elements with the same role and name
    // I've tried to ensure it's not brittle
    await page.locator("form#cancel-request button[type=submit]").click();
    await expect(page).toHaveURL(Paths.YOU_HAVE_CANCELLED_YOUR_REQUEST);
  });

  test("clicking 'No' takes the user to 'Before you start'", async ({
    page,
  }) => {
    // Falling back to a CSS selector here because there are multiple elements with the same role and name
    // I've tried to ensure it's not brittle
    await await page.locator("form#cancel-request a").click();
    await expect(page).toHaveURL(Paths.BEFORE_YOU_START);
  });
});
