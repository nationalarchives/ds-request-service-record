import { test, expect } from "@playwright/test";

test.describe("your postal address", () => {
  const basePath = "/request-a-service-record";

  enum Urls {
    START_PAGE = `${basePath}/start/`,
    YOUR_POSTAL_ADDRESS = `${basePath}/your-postal-address/`,
    YOUR_DETAILS = `${basePath}/your-details/`,
  }

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.START_PAGE);
    await page.goto(Urls.YOUR_POSTAL_ADDRESS);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/Your postal address/);
  });

  test.describe("when submitted", () => {
    test("without the form having been completed, shows relevant errors", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-form__error-message")).toHaveCount(2);
      await expect(page.locator(".tna-form__error-message").first()).toHaveText(
        /First line of your address is required/,
      );
      await expect(page.locator(".tna-form__error-message").nth(1)).toHaveText(
        /Your town or city is required/,
      );
    });

    test("with the form completed, takes the user to the 'How do you want your order processed?' page", async ({
      page,
    }) => {
      await page.getByLabel("Address Line 1").fill("123 Non-existent Road");
      await page.getByLabel("Town or city").fill("Non-existent Town");
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(/how-do-you-want-your-order-processed/);
    });

    test("clicking 'Back' from 'Your postal address' brings the user back to the 'Your details' page", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Urls.YOUR_DETAILS);
    });
  });
});
