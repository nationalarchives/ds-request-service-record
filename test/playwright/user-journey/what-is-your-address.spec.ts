import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("what is your address", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.WHAT_IS_YOUR_ADDRESS);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/What is your address/);
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

    test("with the form completed, takes the user to the 'Your order summary' page", async ({
      page,
    }) => {
      await page.getByLabel("Address Line 1").fill("123 Non-existent Road");
      await page.getByLabel("Town or city").fill("Non-existent Town");
      await page.getByLabel("Postcode").fill("TW9 4DU");
      await page.getByLabel("Country").selectOption("United Kingdom");
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(Paths.YOUR_ORDER_SUMMARY);
    });

    test("clicking 'Back' from 'What is your address' brings the user back to the 'Your contact details' page", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Paths.YOUR_CONTACT_DETAILS);
    });
  });
});
