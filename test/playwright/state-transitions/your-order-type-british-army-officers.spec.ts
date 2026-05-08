import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromBeforeYouStart,
  continueFromHaveYouPreviouslyMadeARequest,
  continueFromHowWeProcessRequests,
  continueFromIsServicePersonAlive,
  continueFromJourneyStart,
  continueFromProvideAProofOfDeath,
  continueFromServicePersonDetails,
  continueFromUploadAProofOfDeath,
  continueFromWeAreUnlikelyToHoldThisRecord,
  continueFromWereTheyACommissionedOfficer,
  continueFromWhatWasTheirDateOfBirth,
  continueFromWhichMilitaryBranchDidThePersonServeIn,
  continueFromYouMayWantToCheckAncestry,
  continueFromYourOrderTypeBritishArmyOfficers,
} from "../lib/step-functions";
import { armyOfficer } from "../end-to-end/test-cases/your-order-type-variants/army-officer";

test.describe("the 'Your order type page for British Army officers' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
  });

  test("works as expected", async ({ page }) => {
    test.setTimeout(120_000); // Increase timeout to 2 minutes for this test because it is end-to-end
    await continueFromJourneyStart(page);
    await continueFromHowWeProcessRequests(page);
    await continueFromBeforeYouStart(page, true);
    await continueFromYouMayWantToCheckAncestry(page);
    await continueFromIsServicePersonAlive(
      page,
      armyOfficer.isAlive,
      Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN,
    );
    await continueFromWhichMilitaryBranchDidThePersonServeIn(
      page,
      armyOfficer.serviceBranch,
      Paths.WERE_THEY_A_COMMISSIONED_OFFICER,
    );
    await continueFromWereTheyACommissionedOfficer(
      page,
      armyOfficer.wasOfficer,
      Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY,
      "unlikely-to-hold--army-officer-records",
    );
    await continueFromWeAreUnlikelyToHoldThisRecord(
      page,
      Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY,
    );
    await continueFromWhatWasTheirDateOfBirth(
      page,
      armyOfficer.dateOfBirth.day,
      armyOfficer.dateOfBirth.month,
      armyOfficer.dateOfBirth.year,
      Paths.PROVIDE_A_PROOF_OF_DEATH,
      true,
      "",
    );
    await continueFromProvideAProofOfDeath(
      page,
      armyOfficer.hasDeathCertificate,
      Paths.UPLOAD_A_PROOF_OF_DEATH,
      "Upload a proof of death",
    );
    await continueFromUploadAProofOfDeath(
      page,
      ".jpg",
      1024 * 1024 * 4, //  4MB
      true,
      "",
    );
    await continueFromServicePersonDetails(page, armyOfficer);
    await continueFromHaveYouPreviouslyMadeARequest(page, {
      label: armyOfficer.hasPreviouslyMadeRequest,
      errorMessage: null,
      populatedReferenceNumber: null,
      nextPath: Paths.YOUR_ORDER_TYPE_BRITISH_ARMY_OFFICERS,
    });
    await continueFromYourOrderTypeBritishArmyOfficers(page);
    // the previous step function results in the user being on "Your contact details"
    // so we check the back link takes them back to the correct order type variant
    await clickBackLink(page, Paths.YOUR_ORDER_TYPE_BRITISH_ARMY_OFFICERS);
  });
});
