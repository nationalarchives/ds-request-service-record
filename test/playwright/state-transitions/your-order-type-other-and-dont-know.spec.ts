import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
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
  continueFromYourOrderTypeOtherAndDontKnowOfficers,
} from "../lib/step-functions";
import { otherOfficer } from "../end-to-end/test-cases/your-order-type-variants/other-officer";
import { unknownOfficer } from "../end-to-end/test-cases/your-order-type-variants/unknown-officer";

test.describe("the 'Your order type for officers where service branch is 'other' or unknown form", () => {
  const scenarios = [{ person: otherOfficer }, { person: unknownOfficer }];

  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
  });

  async function runFromStartPageToYourOrderTypePage(page, person) {
    test.setTimeout(120_000); // End-to-end path

    await continueFromJourneyStart(page);
    await continueFromHowWeProcessRequests(page);
    await continueFromBeforeYouStart(page, true);
    await continueFromYouMayWantToCheckAncestry(page);

    await continueFromIsServicePersonAlive(
      page,
      person.isAlive,
      Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN,
    );

    await continueFromWhichMilitaryBranchDidThePersonServeIn(
      page,
      person.serviceBranch,
      Paths.WERE_THEY_A_COMMISSIONED_OFFICER,
    );

    await continueFromWereTheyACommissionedOfficer(
      page,
      person.wasOfficer,
      Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__GENERIC,
      "we-are-unlikely-to-hold-this-record--generic",
    );

    await continueFromWeAreUnlikelyToHoldThisRecord(
      page,
      Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__GENERIC,
    );

    await continueFromWhatWasTheirDateOfBirth(
      page,
      person.dateOfBirth.day,
      person.dateOfBirth.month,
      person.dateOfBirth.year,
      Paths.PROVIDE_A_PROOF_OF_DEATH,
      true,
      "",
    );

    await continueFromProvideAProofOfDeath(
      page,
      person.hasDeathCertificate,
      Paths.UPLOAD_A_PROOF_OF_DEATH,
      "Upload a proof of death",
    );

    await continueFromUploadAProofOfDeath(
      page,
      ".jpg",
      1024 * 1024 * 4,
      true,
      "",
    );

    await continueFromServicePersonDetails(page, person);

    await continueFromHaveYouPreviouslyMadeARequest(page, {
      label: person.hasPreviouslyMadeRequest,
      errorMessage: null,
      populatedReferenceNumber: null,
      nextPath: Paths.YOUR_ORDER_TYPE_OTHER_AND_DONT_KNOW_OFFICERS,
    });

    await continueFromYourOrderTypeOtherAndDontKnowOfficers(page);
  }

  scenarios.forEach(({ person }) => {
    test(`works as expected when service branch is '${person.serviceBranch}'`, async ({
      page,
    }) => {
      await runFromStartPageToYourOrderTypePage(page, person);
    });
  });
});
