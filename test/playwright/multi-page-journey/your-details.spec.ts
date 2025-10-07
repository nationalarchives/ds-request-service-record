import { test, expect } from "@playwright/test";

test.describe("your details", () => {
  const basePath = "/request-a-service-record";

  enum Urls {
    START_PAGE = `${basePath}/start/`,
    HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST = `${basePath}/have-you-previously-made-a-request/`,
    YOUR_DETAILS = `${basePath}/your-details/`,
    YOUR_POSTAL_ADDRESS = `${basePath}/your-postal-address/`,
    HOW_DO_YOU_WANT_YOUR_ORDER_PROCESSED = `${basePath}/how-do-you-want-your-order-processed/`,
  }

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.START_PAGE);
    await page.goto(Urls.YOUR_DETAILS);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/Your details/);
  });

  test.describe("when submitted", () => {
    test("without the form having been completed, shows an error", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-form-item__error")).toHaveCount(2);
      await expect(page.locator(".tna-form-item__error").first()).toHaveText(
        /Your first name is required/,
      );
      await expect(page.locator(".tna-form-item__error").nth(1)).toHaveText(
        /Your last name is required/,
      );
    });

    test.describe("with the form completed", () => {
      test("takes the user to the 'Your postal address' page if the user doesn't have an email address", async ({
        page,
      }) => {
        await page.getByLabel("First name").fill("John");
        await page.getByLabel("Last name").fill("Doe");
        // TODO: Investigate why we need to force this checkbox to be checked - the label seems to be intercepting pointer events
        await page
          .getByLabel("I do not have an email address")
          .check({ force: true });
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(Urls.YOUR_POSTAL_ADDRESS);
      });
      test("takes the user to the 'How would you like your order processed' page if the user does have an email address", async ({
        page,
      }) => {
        await page.getByLabel("First name").fill("John");
        await page.getByLabel("Last name").fill("Doe");
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(Urls.HOW_DO_YOU_WANT_YOUR_ORDER_PROCESSED);
      });
    });

    test("clicking 'Back' from 'Your details' brings the user back to the 'Have you previously made a request?' page", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Urls.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST);
    });
  });
});
