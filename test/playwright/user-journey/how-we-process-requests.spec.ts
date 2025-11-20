import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'How we process requests' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.HOW_WE_PROCESS_REQUESTS);

  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /How we process requests/,
    );
  });

  test.describe("when the user clicks continue", () => {
    test("takes the user to the 'Before you start' page", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(Paths.BEFORE_YOU_START);
    });
    test("has the correct heading", async ({ page }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(Paths.BEFORE_YOU_START);
      await expect(page.locator("h1")).toHaveText(/Before you start/);
    });
  });

  test("clicking 'Back' from 'Before you start' brings the user back to the 'How we process requests' page", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(Paths.BEFORE_YOU_START);
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Paths.HOW_WE_PROCESS_REQUESTS);
    });
});
