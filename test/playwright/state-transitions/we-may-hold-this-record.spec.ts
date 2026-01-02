import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromWeMayHoldThisRecord,
  checkExternalLink,
} from "../lib/step-functions";

test.describe("the 'We may hold this record' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.WE_MAY_HOLD_THIS_RECORD);
  });

  test("works as expected", async ({ page }) => {
    await continueFromWeMayHoldThisRecord(page);
  });

  test("the FOI link is configured correctly", async ({ page }) => {
    await checkExternalLink(
      page,
      "You can find out more about FOI on GOV.UK (opens in new tab)",
      "https://www.gov.uk/make-a-freedom-of-information-request",
    );
  });

  test.describe("when interacted with", () => {
    test("clicking 'Back' takes the user to 'Were they a commissioned officer?' page", async ({
      page,
    }) => {
      await clickBackLink(page, Paths.WERE_THEY_A_COMMISSIONED_OFFICER);
    });

    test("clicking 'Back' from 'What was their date of birth?' brings the user back to the 'We may hold this record' page", async ({
      page,
    }) => {
      await continueFromWeMayHoldThisRecord(page);
      await clickBackLink(page, Paths.WE_MAY_HOLD_THIS_RECORD);
    });
  });
});
