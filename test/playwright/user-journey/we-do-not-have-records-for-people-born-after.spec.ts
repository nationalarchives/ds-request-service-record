import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("The 'We do not have records for people born after...' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.WE_DO_NOT_HAVE_RECORDS_FOR_PEOPLE_BORN_AFTER);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /We do not have records for people born after 1939/,
    );
  });

  test('clicking "Back" takes the user back to the "What was their date of birth?" page', async ({
    page,
  }) => {
    await page.getByRole("link", { name: "Back" }).click();
    await expect(page).toHaveURL(Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH);
  });

  test.describe("clicking 'Exit this form' button", () => {
    test("takes the user to the 'Are you sure you want to cancel?' page", async ({
      page,
    }) => {
      await page.getByRole("button", { name: "Exit this form" }).click();
      await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
    });

    test("once on 'Are you sure you want to cancel?' page, clicking 'Back' brings the user back", async ({
      page,
    }) => {
      await page.goto(Paths.WE_DO_NOT_HAVE_RECORDS_FOR_PEOPLE_BORN_AFTER);
      await page.getByRole("button", { name: "Exit this form" }).click();
      await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(
        Paths.WE_DO_NOT_HAVE_RECORDS_FOR_PEOPLE_BORN_AFTER,
      );
    });
  });

  test.describe("clicking the 'Request from the Ministry of Defence' link", () => {
    test("opens link in new tab", async ({ page }) => {
      const [newPage] = await Promise.all([
        page.waitForEvent("popup"), // waits for the new tab
        page
          .getByRole("link", { name: "Request from the Ministry of Defence" })
          .click(),
      ]);

      await newPage.waitForLoadState("domcontentloaded");

      expect(newPage.url()).toContain(
        "https://www.gov.uk/get-copy-military-records-of-service/apply-for-the-records-of-a-deceased-serviceperson",
      );
    });
  });
});
