import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromYourContactDetails,
} from "../lib/step-functions";

test.describe("Your contact details", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.YOUR_CONTACT_DETAILS);
  });

  test.describe("works as expected", () => {
    test("when entries do not exceed allowed field lengths, there are no errors", async ({
      page,
    }) => {
      const suppliedDetails = {
        firstName: "a".repeat(128),
        lastName: "a".repeat(128),
        emailAddress: "a".repeat(40) + "@example.com",
      };

      await page.getByLabel("First name").fill(suppliedDetails.firstName);
      await page.getByLabel("Last name").fill(suppliedDetails.lastName);
      await page.locator("#requester_email").fill(suppliedDetails.emailAddress);
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-form-item__error")).toHaveCount(0);
    });

    test("when the user has an email address", async ({ page }) => {
      await continueFromYourContactDetails(page, {
        firstName: "Hilary",
        lastName: "Jenkinson",
        emailAddress: "test@example.com",
      });
      await clickBackLink(page, Paths.YOUR_CONTACT_DETAILS);
    });
    test("when the user does not have an email address", async ({ page }) => {
      await continueFromYourContactDetails(page, {
        firstName: "Hilary",
        lastName: "Jenkinson",
      });
      await clickBackLink(page, Paths.YOUR_CONTACT_DETAILS);
    });
  });

  // In the interests of keeping the step functions simple, I've decided to keep the validation
  // failure scenarios here. There are just too many permutations to make it worth trying to
  // encapsulate them in the step function for this page.

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
        /Enter an email address in the correct format like name@example.com, or select 'I do not have an email address'/,
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
        /Enter an email address in the correct format like name@example.com, or select 'I do not have an email address'/,
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
        /Email must be blank if you have selected 'I do not have an email address'/,
      );
    });

    test("when entries exceed allowed field lengths, there are errors", async ({
      page,
    }) => {
      const suppliedDetails = {
        firstName: "a".repeat(129),
        lastName: "a".repeat(129),
        emailAddress: "a".repeat(256) + "@example.com",
      };

      await page.getByLabel("First name").fill(suppliedDetails.firstName);
      await page.getByLabel("Last name").fill(suppliedDetails.lastName);
      await page.locator("#requester_email").fill(suppliedDetails.emailAddress);
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-form-item__error")).toHaveCount(3);

      const errors = page.locator(".tna-form-item__error");
      for (const error of await errors.all()) {
        await expect(error).toContainText(/characters or less/i);
      }
    });
  });
});
