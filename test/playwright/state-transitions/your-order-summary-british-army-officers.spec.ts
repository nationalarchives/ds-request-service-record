import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  continueFromBeforeYouStart,
  continueFromHaveYouPreviouslyMadeARequest,
  continueFromHowWeProcessRequests,
  continueFromIsServicePersonAlive,
  continueFromJourneyStart,
  continueFromServicePersonDetails,
  continueFromWeAreUnlikelyToHoldThisRecord,
  continueFromWereTheyACommissionedOfficer,
  continueFromWhatWasTheirDateOfBirth,
  continueFromWhichMilitaryBranchDidThePersonServeIn,
  continueFromYouMayWantToCheckAncestry,
  continueFromYourContactDetails,
  continueFromYourOrderTypeBritishArmyOfficers,
  continueFromYourPostalAddress,
} from "../lib/step-functions";

// There are dedicated "Your order summary" pages for British Army Commissioned Officers. One is for Digital and one is for Printed.
// This test file is specifically to test the journey to these pages and what is shown on them. The other test file (your-order-summary.spec.ts)
// covers the other combinations (where the variant is simply based on the order type and delivery method).
test.describe("Routes to 'Your order summary' pages specific to British Army Commissioned Officers", () => {
  test.beforeEach(async ({ page }) => {
    test.setTimeout(120_000); // Increase timeout to 2 minutes for this test because it is end-to-end
    await page.goto(Paths.JOURNEY_START);
    await continueFromJourneyStart(page);
    await continueFromHowWeProcessRequests(page);
    await continueFromBeforeYouStart(page, true);
    await continueFromYouMayWantToCheckAncestry(page);
    await continueFromIsServicePersonAlive(
      page,
      "No",
      Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN,
    );
    await continueFromWhichMilitaryBranchDidThePersonServeIn(
      page,
      "British Army",
      Paths.WERE_THEY_A_COMMISSIONED_OFFICER,
    );
    await continueFromWereTheyACommissionedOfficer(
      page,
      "Yes",
      Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY,
      "unlikely-to-hold--army-officer-records",
    );
    await continueFromWeAreUnlikelyToHoldThisRecord(
      page,
      Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY,
    );
    await continueFromWhatWasTheirDateOfBirth(
      page,
      "01",
      "01",
      "1900",
      Paths.SERVICE_PERSON_DETAILS,
    );
    await continueFromServicePersonDetails(page, {
      firstName: "Francis",
      lastName: "Palgrave",
    });
    await continueFromHaveYouPreviouslyMadeARequest(page, {
      label: "No",
      nextPath: Paths.YOUR_ORDER_TYPE_BRITISH_ARMY_OFFICERS,
    });
    await continueFromYourOrderTypeBritishArmyOfficers(page);
  });

  test.describe("we're presenting the correct information for British Army Commissioned Officer Full Record Check order when", () => {
    test("provided digitally", async ({ page }) => {
      await continueFromYourContactDetails(page, {
        firstName: "Leslie",
        lastName: "Request",
        emailAddress: "test@example.com",
      });

      await expect(page.locator("[data-price]")).toHaveText("£48.87");
      await expect(page.locator("[data-second-payment-details]")).toContainText(
        "£1.52 per page",
      );
    });

    test("provided by post", async ({ page }) => {
      await continueFromYourContactDetails(page, {
        firstName: "Leslie",
        lastName: "Request",
      });

      await continueFromYourPostalAddress(page);

      await expect(page.locator("[data-price]")).toHaveText("£48.87");
      await expect(page.locator("[data-second-payment-details]")).toContainText(
        "£7.40 per printed page",
      );
    });
  });
});
