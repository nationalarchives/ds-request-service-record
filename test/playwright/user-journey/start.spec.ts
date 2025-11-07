import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the service start form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /Request a military service record/,
    );
  });

  test.describe("when the user clicks continue", () => {
    test("takes the user to the 'How the process works' page", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Start now/i }).click();
      await expect(page).toHaveURL(Paths.HOW_THE_PROCESS_WORKS);
    });
    test("has the correct heading", async ({ page }) => {
      await page.getByRole("button", { name: /Start now/i }).click();
      await expect(page).toHaveURL(Paths.HOW_THE_PROCESS_WORKS);
      await expect(page.locator("h1")).toHaveText(/How the process works/);
    });
  });
});
