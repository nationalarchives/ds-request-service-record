import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("Your order summary", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.YOUR_ORDER_SUMMARY);
  });

  test.describe("when first rendered", () => {
    test("has the correct heading", async ({ page }) => {
      await expect(page.locator("h1")).toHaveText(/Your order summary/);
    });
  });

  test.describe("when interacted with", () => {
    test("clicking the 'Back' link takes the user to 'Your contact details'", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Paths.YOUR_CONTACT_DETAILS);
    });

    test.describe("the 'Change order' link", () => {
      test("takes the user to the 'Choose your order type' page", async ({
        page,
      }) => {
        await page.getByRole("link", { name: "Change order" }).click();
        await expect(page).toHaveURL(Paths.CHOOSE_YOUR_ORDER_TYPE);
      });

      test("having reached the 'Choose your order type' page, clicking 'Back' brings the user back here", async ({
        page,
      }) => {
        await page.getByRole("link", { name: "Change order" }).click();
        await expect(page).toHaveURL(Paths.CHOOSE_YOUR_ORDER_TYPE);
        await page.getByRole("link", { name: "Back" }).click();
        await expect(page).toHaveURL(Paths.YOUR_ORDER_SUMMARY);
      });
    });
  });
});
