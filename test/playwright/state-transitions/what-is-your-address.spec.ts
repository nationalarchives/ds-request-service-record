import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromYourPostalAddress,
} from "../lib/step-functions";

test.describe("what is your address", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.WHAT_IS_YOUR_ADDRESS);
  });

  test("works as expected", async ({ page }) => {
    await continueFromYourPostalAddress(page);
    await clickBackLink(page, Paths.WHAT_IS_YOUR_ADDRESS);
  });

  test.describe("when submitted", () => {
    test("without the form having been completed, shows relevant errors", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-form-item__error")).toHaveCount(4);
      await expect(page.locator(".tna-form-item__error").first()).toHaveText(
        /Enter address line 1, typically the building and street/,
      );
      await expect(page.locator(".tna-form-item__error").nth(1)).toHaveText(
        /Enter town or city/,
      );
      await expect(page.locator(".tna-form-item__error").nth(2)).toHaveText(
        /Enter postcode/,
      );
      await expect(page.locator(".tna-form-item__error").nth(3)).toHaveText(
        /Select a country from the list/,
      );
    });
  });
});
