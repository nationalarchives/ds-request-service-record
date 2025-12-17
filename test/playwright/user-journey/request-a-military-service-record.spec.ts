import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'Request a military service record' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
  });

  test.describe("when first rendered", () => {
    test("has the correct heading", async ({ page }) => {
      await expect(page.locator("h1")).toHaveText(
        /Request a military service record/,
      );
    });
  });

  test.describe("when clicking 'Continue'", () => {
    test("takes the user to the 'How we process requests' page", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(Paths.HOW_WE_PROCESS_REQUESTS);
    });
    test("has the correct heading", async ({ page }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(Paths.HOW_WE_PROCESS_REQUESTS);
    });
    test("clicking the 'Back' link on the next page brings the user back", async ({ page }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(Paths.HOW_WE_PROCESS_REQUESTS);
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Paths.JOURNEY_START);
    });
  });
});
