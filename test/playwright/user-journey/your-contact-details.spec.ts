import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("Your contact details", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.YOUR_CONTACT_DETAILS);
  });

  test.describe("when first rendered", () => {
    test("has the correct heading", async ({ page }) => {
      await expect(page.locator("h1")).toHaveText(/Your contact details/);
    });
  });

  test.describe("when submitted", () => {
    test.describe("with the form completed", () => {
      test("takes the user to the 'What is your address?' page if the user doesn't have an email address", async ({
        page,
      }) => {
        await page.getByLabel("First name").fill("John");
        await page.getByLabel("Last name").fill("Doe");
        await page
          .getByLabel("I do not have an email address")
          .check({ force: true });
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(Paths.WHAT_IS_YOUR_ADDRESS);
      });
      test("takes the user to the 'Choose your order type' page if the user does have an email address", async ({
        page,
      }) => {
        await page.getByLabel("First name").fill("John");
        await page.getByLabel("Last name").fill("Doe");
        await page.getByLabel("Email", { exact: true }).fill("john@doe.com");
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(Paths.YOUR_ORDER_SUMMARY);
      });
    });

    test.describe("validation failure scenarios", () => {
      test("without the form having been completed at all, shows an error", async ({
        page,
      }) => {
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page.locator(".tna-form-item__error")).toHaveCount(3);
        await expect(page.locator(".tna-form-item__error").first()).toHaveText(
          /Enter your first name/,
        );
        await expect(page.locator(".tna-form-item__error").nth(1)).toHaveText(
          /Enter your last name/,
        );
        await expect(page.locator(".tna-form-item__error").nth(2)).toHaveText(
          /Enter an email address in the correct format, like name@example.com. If you do not have an email address, please select 'I do not have an email address' below/,
        );
      });

      test("with names provided but no information about email, shows an error", async ({
        page,
      }) => {
        await page.getByLabel("First name").fill("Francis");
        await page.getByLabel("Last name").fill("Palgrave");
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page.locator(".tna-form-item__error")).toHaveCount(1);
        await expect(page.locator(".tna-form-item__error").first()).toHaveText(
          /Enter an email address in the correct format, like name@example.com. If you do not have an email address, please select 'I do not have an email address' below/,
        );
      });

      test("with 'I do not have an email' checked but no names provided, shows an error", async ({
        page,
      }) => {
        await page
          .getByLabel("I do not have an email address")
          .check({ force: true });
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page.locator(".tna-form-item__error")).toHaveCount(2);
        await expect(page.locator(".tna-form-item__error").first()).toHaveText(
          /Enter your first name/,
        );
        await expect(page.locator(".tna-form-item__error").nth(1)).toHaveText(
          /Enter your last name/,
        );
      });

      test("with names provided but an invalid email, shows an error", async ({
        page,
      }) => {
        await page.getByLabel("First name").fill("Francis");
        await page.getByLabel("Last name").fill("Palgrave");
        await page.locator("#requester_email").fill("my email address");
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page.locator(".tna-form-item__error")).toHaveCount(1);
        await expect(page.locator(".tna-form-item__error").first()).toHaveText(
          /Enter an email address in the correct format, like name@example.com/,
        );
      });

      test("with 'I do not have an email' checked and an email provided, shows an error", async ({
        page,
      }) => {
        await page.getByLabel("First name").fill("Francis");
        await page.getByLabel("Last name").fill("Palgrave");
        await page.locator("#requester_email").fill("test@example.com");
        await page
          .getByLabel("I do not have an email address")
          .check({ force: true });
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page.locator(".tna-form-item__error")).toHaveCount(1);
        await expect(page.locator(".tna-form-item__error").first()).toHaveText(
          /You have indicated that you do not have an email address. Please leave this field empty/,
        );
      });
    });

    // test("clicking 'Back' from 'Your contact details' brings the user back to the 'Choose your order type' page", async ({
    //   page,
    // }) => {
    //   await page.getByRole("link", { name: "Back" }).click();
    //   await expect(page).toHaveURL(Paths.CHOOSE_YOUR_ORDER_TYPE);
    // });
  });
});
