import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromBeforeYouStart,
  continueFromHaveYouPreviouslyMadeARequest,
  continueFromHowWeProcessRequests,
  continueFromIsServicePersonAlive,
  continueFromJourneyStart,
  continueFromServicePersonDetails,
  continueFromWeMayHoldThisRecord,
  continueFromWereTheyACommissionedOfficer,
  continueFromWhatWasTheirDateOfBirth,
  continueFromWhichMilitaryBranchDidThePersonServeIn,
  continueFromYouMayWantToCheckAncestry,
  continueFromChooseYourOrderTypeRAFNonOfficer,
} from "../lib/step-functions";
import {
  rafNonOfficer,
  rafNonOfficerWithPODWarning,
} from "../end-to-end/test-cases/your-order-type-variants/raf-non-officer";

test.describe("the 'Choose your order type' form for RAF non-officers", () => {
  const scenarios = [rafNonOfficer, rafNonOfficerWithPODWarning];

  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
  });

  for (const person of scenarios) {
    test(`works as expected when proof of death warning is ${person.seesProofOfDeathWarning ? "shown" : "not shown"}`, async ({
      page,
    }) => {
      test.setTimeout(120_000); // Increase timeout to 2 minutes for this test because it is end-to-end
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
        Paths.WE_MAY_HOLD_THIS_RECORD,
        "we-may-hold-this-record--generic",
      );
      await continueFromWeMayHoldThisRecord(
        page,
        Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH,
      );
      await continueFromWhatWasTheirDateOfBirth(
        page,
        person.dateOfBirth.day,
        person.dateOfBirth.month,
        person.dateOfBirth.year,
        Paths.SERVICE_PERSON_DETAILS,
        true,
        "",
      );
      await continueFromServicePersonDetails(page, person);
      await continueFromHaveYouPreviouslyMadeARequest(page, {
        label: person.hasPreviouslyMadeRequest,
        errorMessage: null,
        populatedReferenceNumber: null,
        nextPath: Paths.CHOOSE_YOUR_ORDER_TYPE_RAF_NON_OFFICER,
      });
      await continueFromChooseYourOrderTypeRAFNonOfficer(
        page,
        person.chooseYourOrderTypeSelection,
        Paths.PROVIDE_A_PROOF_OF_DEATH,
        person.seesProofOfDeathWarning,
      );
      // We check the back link takes them back to the correct order type variant
      await clickBackLink(page, Paths.CHOOSE_YOUR_ORDER_TYPE_RAF_NON_OFFICER);
    });
  }
});
