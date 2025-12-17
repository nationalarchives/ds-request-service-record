import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("choose your order type", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.CHOOSE_YOUR_ORDER_TYPE);
  });

  test.describe("when first rendered", () => {
    test("has the correct heading", async ({ page }) => {
      await expect(page.locator("h1")).toHaveText(/Choose your order type/);
    });
  });

  test.describe("when interacted with", () => {
    // test("clicking 'Back' from 'Choose your order type' brings the user back to the 'Have you previously made a request' page", async ({
    //   page,
    // }) => {
    //   await page.getByRole("link", { name: "Back" }).click();
    //   await expect(page).toHaveURL(Paths.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST);
    // });

    test.describe("when submitted", () => {
      test.describe("with the 'Choose standard' option", () => {
        test("the user is taken to 'Your contact details'", async ({
          page,
        }) => {
          await page.getByRole("button", { name: /Choose standard/i }).click();
          await expect(page).toHaveURL(Paths.YOUR_CONTACT_DETAILS);
        });
      });
      test.describe("with the 'Choose full record check' option", () => {
        test("the user is taken to 'Your contact details'", async ({
          page,
        }) => {
          await page
            .getByRole("button", { name: /Choose full record check/i })
            .click();
          await expect(page).toHaveURL(Paths.YOUR_CONTACT_DETAILS);
        });
      });
    });
  });
});
