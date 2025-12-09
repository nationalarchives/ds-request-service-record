import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("your postal address", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.YOUR_POSTAL_ADDRESS);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/Your postal address/);
  });

  test.describe("when submitted", () => {
    test("without the form having been completed, shows relevant errors", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-form-item__error")).toHaveCount(2);
      await expect(page.locator(".tna-form-item__error").first()).toHaveText(
        /Enter address line 1, typically the building and street/,
      );
      await expect(page.locator(".tna-form-item__error").nth(1)).toHaveText(
        /Enter town or city/,
      );
    });

    test("with the form completed, takes the user to the 'How do you want your order processed?' page", async ({
      page,
    }) => {
      await page.getByLabel("Address Line 1").fill("123 Non-existent Road");
      await page.getByLabel("Town or city").fill("Non-existent Town");
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(/choose-your-order-type/);
    });

    test("clicking 'Back' from 'Your postal address' brings the user back to the 'Your details' page", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Paths.YOUR_DETAILS);
    });
  });
});
