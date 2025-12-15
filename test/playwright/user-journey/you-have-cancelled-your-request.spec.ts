import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'You have cancelled your request' page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.YOU_HAVE_CANCELLED_YOUR_REQUEST);
  });

  test.describe("when first rendered", () => {
    test("has the correct heading", async ({ page }) => {
      await expect(page.locator("h1")).toHaveText(
        /You have cancelled your request/,
      );
    });
  });

  test.describe("when interacted with", () => {
    test("clicking 'Start a new request' takes the user to the start page", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Start a new request" }).click();
      await expect(page).toHaveURL(Paths.JOURNEY_START);
    });
  });
});
