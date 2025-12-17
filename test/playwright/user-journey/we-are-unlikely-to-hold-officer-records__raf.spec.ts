import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("The variant of 'We are unlikely to hold this record' for RAF Officers", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__RAF);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /We are unlikely to hold this record/,
    );
  });

  test("presents the correct exceptions to the rule", async ({ page }) => {
    const exceptions = [/Royal Air Force/];
    const exceptionsList = page.locator("#exceptions-list");
    await Promise.all(
      exceptions.map((exception) =>
        expect(exceptionsList).toContainText(exception),
      ),
    );
  });

  test.describe("when interacted with", () => {
    // test('clicking "Back" takes the user back to the "Were they a commissioned officer?" page', async ({
    //   page,
    // }) => {
    //   await page.getByRole("link", { name: "Back" }).click();
    //   await expect(page).toHaveURL(Paths.WERE_THEY_A_COMMISSIONED_OFFICER);
    // });

    test.describe("clicking 'Continue this request' button", () => {
      test("takes the user to the 'What was their date of birth?' page", async ({
        page,
      }) => {
        await page
          .getByRole("button", { name: "Continue this request" })
          .click();
        await expect(page).toHaveURL(Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH);
      });

      // test("once on 'What was their date of birth?' page, clicking 'Back' brings the user back", async ({
      //   page,
      // }) => {
      //   await page.goto(Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__RAF);
      //   await page
      //     .getByRole("button", { name: "Continue this request" })
      //     .click();
      //   await expect(page).toHaveURL(Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH);
      //   await page.getByRole("link", { name: "Back" }).click();
      //   await expect(page).toHaveURL(
      //     Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__RAF,
      //   );
      // });
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
});
