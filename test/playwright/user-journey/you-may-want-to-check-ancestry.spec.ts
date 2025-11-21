import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'You may want to check ancestry' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.YOU_MAY_WANT_TO_CHECK_ANCESTRY);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /You may want to check Ancestry/,
    );
  });

  test.describe("when the user clicks continue", () => {
    test("takes the user to the 'Is the service person alive' form", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(Paths.IS_SERVICE_PERSON_ALIVE);
      await expect(page.locator("h1")).toHaveText(
        /Is the service person alive/,
      );
    });
    test("clicking the 'Back' link takes the user to 'Before you start'", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Paths.BEFORE_YOU_START);
    });
  });
});
