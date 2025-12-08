import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("have you previously made a request", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /Have you previously made a request/,
    );
  });

  test.describe("when submitted", () => {
    test("the user is taken to the 'Your details' page", async ({ page }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(Paths.YOUR_DETAILS);
      await expect(page.locator("h1")).toHaveText(/Your details/);
    });

    test("clicking 'Back' from 'Have you previously made a request for this record? ' brings the user back to the 'Service person details' page", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Paths.SERVICE_PERSON_DETAILS);
    });
  });
});
