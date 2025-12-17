import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'How we process requests' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.HOW_WE_PROCESS_REQUESTS);
  });

  test.describe("when first rendered", () => {
    test("has the correct heading", async ({ page }) => {
      await expect(page.locator("h1")).toHaveText(/How we process requests/);
    });
  });

  test("clicking 'Back' takes the user to 'Request a military service record'", async ({
    page,
  }) => {
    await page.getByRole("link", { name: "Back" }).click();
    await expect(page).toHaveURL(Paths.JOURNEY_START);
  });

  test.describe("when clicking 'Continue'", () => {
    test("the user is taken to the 'Before you start' page", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(Paths.BEFORE_YOU_START);
    });
    // test("clicking 'Back' from the 'Before you start' page brings the user back", async ({
    //   page,
    // }) => {
    //   await page.getByRole("button", { name: /Continue/i }).click();
    //   await expect(page).toHaveURL(Paths.BEFORE_YOU_START);
    //   await page.getByRole("link", { name: "Back" }).click();
    //   await expect(page).toHaveURL(Paths.HOW_WE_PROCESS_REQUESTS);
    // });
  });
});
