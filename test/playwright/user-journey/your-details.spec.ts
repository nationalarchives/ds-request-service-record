import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
test.describe("your details", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.YOUR_DETAILS);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/Your details/);
  });

  test.describe("when submitted", () => {
    test("without the form having been completed, shows an error", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-form-item__error")).toHaveCount(3);
      await expect(page.locator(".tna-form-item__error").first()).toHaveText(
        /Your first name is required/,
      );
      await expect(page.locator(".tna-form-item__error").nth(1)).toHaveText(
        /Your last name is required/,
      );
      await expect(page.locator(".tna-form-item__error").nth(2)).toHaveText(
        /Your email address is required so that we can contact you. If you do not have an email address, please select 'I do not have an email address' below/,
      );
    });

    test.describe("with the form completed", () => {
      test("takes the user to the 'Your postal address' page if the user doesn't have an email address", async ({
        page,
      }) => {
        await page.getByLabel("First name").fill("John");
        await page.getByLabel("Last name").fill("Doe");
        // TODO: Investigate why we need to force this checkbox to be checked - the label seems to be intercepting pointer events
        // Update 16 October 2025:
        // - Spent some time today investigating this but it's not clear what's causing the issue.
        // - Some online searching suggests interception of pointer events seems is affecting other Playwright users too.
        // - What I did find is that replacing `.check()` with `.dispatchEvent('click')` fixes the problem, so that's something
        //   we might want to try if we can't get to the bottom of this.
        await page
          .getByLabel("I do not have an email address")
          .check({ force: true });
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(Paths.YOUR_POSTAL_ADDRESS);
      });
      test("takes the user to the 'How would you like your order processed' page if the user does have an email address", async ({
        page,
      }) => {
        await page.getByLabel("First name").fill("John");
        await page.getByLabel("Last name").fill("Doe");
        await page.getByLabel("Email", { exact: true }).fill("john@doe.com");
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(
          Paths.HOW_DO_YOU_WANT_YOUR_ORDER_PROCESSED,
        );
      });
    });

    test("clicking 'Back' from 'Your details' brings the user back to the 'Have you previously made a request?' page", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Paths.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST);
    });
  });
});
