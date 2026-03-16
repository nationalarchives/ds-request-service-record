import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'Sorry, you will have to start again' page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.SORRY_YOU_WILL_HAVE_TO_START_AGAIN);
  });

  test.describe("presents the correct template", () => {
    test("displays the correct URL and heading", async ({ page }) => {
      await expect(page).toHaveURL(Paths.SORRY_YOU_WILL_HAVE_TO_START_AGAIN);
      await expect(page.locator("h1")).toHaveText(
        /Sorry, you will have to start again/,
      );
    });
  });

  test.describe("clicking the 'Start again' button", () => {
    test("takes the user back to the journey start", async ({ page }) => {
      await page.getByRole("button", { name: /Start again/i }).click();
      await expect(page).toHaveURL(Paths.JOURNEY_START);
    });
  });
});
