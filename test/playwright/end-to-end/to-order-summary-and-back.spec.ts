import { test, expect } from "@playwright/test";
import {
  continueFromBeforeYouStart,
  continueFromHowWeProcessRequests,
  continueFromIsServicePersonAlive,
  continueFromJourneyStart,
  continueFromWereTheyACommissionedOfficer,
  continueFromWhichMilitaryBranchDidThePersonServeIn,
  continueFromYouMayWantToCheckAncestry,
  continueFromWeMayHoldThisRecord,
  continueFromWhatWasTheirDateOfBirth,
  continueFromProvideAProofOfDeath,
  continueFromUploadAProofOfDeath,
  continueFromServicePersonDetails,
  continueFromHaveYouPreviouslyMadeARequest,
  continueFromChooseYourOrderType,
  continueFromYourContactDetails,
  clickBackLink,
} from "../lib/step-functions";
import { Paths } from "../lib/constants";
import { robertHughJones } from "./test-cases/robert-hugh-jones";

test.describe("End-to-end journey", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
  });
  test.describe("from 'Request a military service record' to 'Your order summary' and back", () => {
    test("works as expected", async ({ page }) => {
      test.setTimeout(120_000); // Increase timeout to 2 minutes for this test because it is end-to-end
      await continueFromJourneyStart(page);
      await continueFromHowWeProcessRequests(page);
      await continueFromBeforeYouStart(page, true);
      await continueFromYouMayWantToCheckAncestry(page);
      await continueFromIsServicePersonAlive(
        page,
        robertHughJones.isAlive,
        Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN,
      );
      await continueFromWhichMilitaryBranchDidThePersonServeIn(
        page,
        robertHughJones.serviceBranch,
        Paths.WERE_THEY_A_COMMISSIONED_OFFICER,
      );
      await continueFromWereTheyACommissionedOfficer(
        page,
        robertHughJones.wasOfficer,
        Paths.WE_MAY_HOLD_THIS_RECORD,
        "we-may-hold-this-record--generic",
      );
      await continueFromWeMayHoldThisRecord(page);
      await continueFromWhatWasTheirDateOfBirth(
        page,
        robertHughJones.dateOfBirth.day,
        robertHughJones.dateOfBirth.month,
        robertHughJones.dateOfBirth.year,
        Paths.PROVIDE_A_PROOF_OF_DEATH,
        true,
        "",
      );
      await continueFromProvideAProofOfDeath(
        page,
        robertHughJones.hasDeathCertificate,
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
      await continueFromServicePersonDetails(page, robertHughJones);
      await continueFromHaveYouPreviouslyMadeARequest(
        page,
        robertHughJones.hasPreviouslyMadeRequest,
      );
      await continueFromChooseYourOrderType(
        page,
        robertHughJones.orderSelection,
      );
      await continueFromYourContactDetails(
        page,
        robertHughJones.personMakingRequest,
      );
      await expect(page.locator("#processing-option")).toHaveText(
        new RegExp("Standard"),
      );
      await expect(page.locator("#price")).toHaveText(new RegExp("£42.25"));
      // And now we go back up the journey to check all the back links work as expected
      await clickBackLink(page, Paths.YOUR_CONTACT_DETAILS);
      await clickBackLink(page, Paths.CHOOSE_YOUR_ORDER_TYPE);
      await clickBackLink(page, Paths.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST);
      await clickBackLink(page, Paths.SERVICE_PERSON_DETAILS);
      await clickBackLink(page, Paths.UPLOAD_A_PROOF_OF_DEATH);
      await clickBackLink(page, Paths.PROVIDE_A_PROOF_OF_DEATH);
      await clickBackLink(page, Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH);
      await clickBackLink(page, Paths.WE_MAY_HOLD_THIS_RECORD);
      await clickBackLink(page, Paths.WERE_THEY_A_COMMISSIONED_OFFICER);
      await clickBackLink(
        page,
        Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN,
      );
      await clickBackLink(page, Paths.IS_SERVICE_PERSON_ALIVE);
      await clickBackLink(page, Paths.YOU_MAY_WANT_TO_CHECK_ANCESTRY);
      await clickBackLink(page, Paths.BEFORE_YOU_START);
      await clickBackLink(page, Paths.HOW_WE_PROCESS_REQUESTS);
      await clickBackLink(page, Paths.JOURNEY_START);
    });
  });
});
