import { test, expect } from "@playwright/test";

test.describe("your details", () => {
  const basePath = "/request-a-service-record";
  enum Urls {
    START_PAGE = `${basePath}/start/`,
    HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST = `${basePath}/have-you-previously-made-a-request/`,
    YOUR_DETAILS = `${basePath}/your-details/`,
  }

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.START_PAGE);
    await page.goto(Urls.YOUR_DETAILS);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/Your details/);
  });

  test.describe("when submitted", () => {
    test("without a submission, shows an error", async ({ page }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-form__error-message")).toHaveCount(2);
      await expect(page.locator(".tna-form__error-message").first()).toHaveText(
        /Your first name is required/,
      );
      await expect(page.locator(".tna-form__error-message").nth(1)).toHaveText(
        /Your last name is required/,
      );
    });

    test("clicking 'Back' from 'Have you previously made a request?' brings the user back to the 'Service person details' page", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Urls.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST);
    });
  });
});
