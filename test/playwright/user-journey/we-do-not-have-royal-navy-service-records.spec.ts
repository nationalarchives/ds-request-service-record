import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'We do not hold this record' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS);
  });

  test.describe("when first rendered", () => {
    test("has the correct heading", async ({ page }) => {
      await expect(page.locator("h1")).toHaveText(/We do not hold this record/);
    });
  });

  test.describe("when interacted with", () => {

    test("clicking the 'Back' link takes the user to 'Which military branch did the person serve in?'", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(
        Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN,
      );
    });

    test.describe("clicking the 'Request from the Ministry of Defence' button", () => {
      test("opens link in new tab", async ({ page }) => {
        // Trigger that opens a new tab (e.g. <a target="_blank">)
        const [newPage] = await Promise.all([
          page.waitForEvent("popup"), // waits for the new tab
          page
            .getByRole("link", { name: "Request from the Ministry of Defence" })
            .click(),
        ]);

        await newPage.waitForLoadState("domcontentloaded");

        // Assertions on the new tab
        expect(newPage.url()).toContain(
          "https://www.gov.uk/get-copy-military-records-of-service/apply-for-the-records-of-a-deceased-serviceperson",
        );
      });
    });

    test("clicking the 'Exit this form' button takes the user to 'Are you sure you want to cancel?'", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Exit this form/i }).click();
      await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
    });

    test("clicking the 'Back' link on 'Are you sure you want to cancel? page brings the user back'", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Exit this form/i }).click();
      await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(
        Paths.WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS,
      );
    });

    test("clicking the 'No' link on 'Are you sure you want to cancel? page brings the user back'", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Exit this form/i }).click();
      await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
      // Falling back to a CSS selector here because there are multiple elements with the same role and name
      // I've tried to ensure it's not brittle
      await page.locator("form#cancel-request a").click();
      await expect(page).toHaveURL(
        Paths.WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS,
      );
    });
  });
});
