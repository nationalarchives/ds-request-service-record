import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'We may hold this record' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Paths.WE_MAY_HOLD_THIS_RECORD);
  });

  test.describe("when first rendered", () => {
    test("has the correct heading", async ({ page }) => {
      await expect(page.locator("h1")).toHaveText(/We may hold this record/);
    });
  });

  test.describe("when interacted with", () => {
    test.describe("clicking the 'You can find out more about FOI on GOV.UK (opens in a new tab)' button", () => {
      test("opens link in new tab", async ({ page }) => {
        // Trigger that opens a new tab (e.g. <a target="_blank">)
        const [newPage] = await Promise.all([
          page.waitForEvent("popup"), // waits for the new tab
          page
            .getByRole("link", {
              name: "You can find out more about FOI on GOV.UK (opens in new tab)",
            })
            .click(),
        ]);

        await newPage.waitForLoadState("domcontentloaded");

        // Assertions on the new tab
        expect(newPage.url()).toContain(
          "https://www.gov.uk/make-a-freedom-of-information-request",
        );
      });
    });

    test.describe("when submitted", () => {
      test("the user is taken to the 'What was their date of birth?' page", async ({
        page,
      }) => {
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH);
        await expect(page.locator("h1")).toHaveText(
          /What was their date of birth?/,
        );
      });

      test("clicking 'Back' from 'What was their date of birth?' brings the user back to the 'We may hold this record' page", async ({
        page,
      }) => {
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH);
        await page.getByRole("link", { name: "Back" }).click();
        await expect(page).toHaveURL(Paths.WE_MAY_HOLD_THIS_RECORD);
      });
    });
  });
});
