import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  checkExternalLink,
  clickBackLink,
  continueFromWeAreUnlikelyToHoldThisRecord,
} from "../lib/step-functions";

test.describe("The variant of 'We are unlikely to hold this record' for Army Officers", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__RAF);
  });

  test("the 'Request from the Ministry of Defence' link is correct", async ({
    page,
  }) => {
    await checkExternalLink(
      page,
      "Request from the Ministry of Defence",
      "https://www.gov.uk/get-copy-military-records-of-service/apply-for-the-records-of-a-deceased-serviceperson",
    );
  });

  test("works as expected", async ({ page }) => {
    await continueFromWeAreUnlikelyToHoldThisRecord(
      page,
      Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__RAF,
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
    test('clicking "Back" takes the user back to the "Were they a commissioned officer?" page', async ({
      page,
    }) => {
      await clickBackLink(page, Paths.WERE_THEY_A_COMMISSIONED_OFFICER);
    });
    test("once on 'What was their date of birth?' page, clicking 'Back' brings the user back", async ({
      page,
    }) => {
      await continueFromWeAreUnlikelyToHoldThisRecord(
        page,
        Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__RAF,
      );
      await clickBackLink(
        page,
        Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__RAF,
      );
    });
  });
});
