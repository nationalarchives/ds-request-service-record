import { test } from "@playwright/test";
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
} from "../lib/step-functions";
import { Paths } from "../lib/constants";

test.describe("End-to-end journey", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
  });
  test.describe("from 'Request a military service record' to 'Your order summary' and back", () => {
    test("works as expected", async ({ page }) => {
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
        "No",
        Paths.WE_MAY_HOLD_THIS_RECORD,
        "we-may-hold-this-record--generic",
      );
      await continueFromWeMayHoldThisRecord(page);
      await continueFromWhatWasTheirDateOfBirth(
        page,
        "15",
        "06",
        "1914",
        Paths.PROVIDE_A_PROOF_OF_DEATH,
        true,
        "",
      );
      await continueFromProvideAProofOfDeath(
        page,
        "Yes",
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
    });
  });
});
