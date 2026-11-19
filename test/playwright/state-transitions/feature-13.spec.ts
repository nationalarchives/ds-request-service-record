import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromWeMayHoldThisRecord,
  continueFromWereTheyACommissionedOfficer,
  continueFromWhichMilitaryBranchDidThePersonServeIn,
} from "../lib/step-functions";

test.describe("Feature 13 enabled", () => {
  // The app must also be started with ENABLE_FEATURE_13=True.
  test.skip(
    process.env.ENABLE_FEATURE_13 !== "True",
    "Run separately against an app with Feature 13 enabled",
  );

  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN);
  });

  test("Army officers reach 'We may hold this record' and can navigate back", async ({
    page,
  }) => {
    await continueFromWhichMilitaryBranchDidThePersonServeIn(
      page,
      "British Army",
    );
    await continueFromWereTheyACommissionedOfficer(
      page,
      "Yes",
      Paths.WE_MAY_HOLD_THIS_RECORD,
      "we-may-hold-this-record--generic",
    );
    await continueFromWeMayHoldThisRecord(page);
    await clickBackLink(page, Paths.WE_MAY_HOLD_THIS_RECORD);
    await clickBackLink(page, Paths.WERE_THEY_A_COMMISSIONED_OFFICER);
  });

  const unchangedJourneys = [
    {
      branch: "British Army",
      officer: "No",
      destination: Paths.WE_MAY_HOLD_THIS_RECORD,
      template: "we-may-hold-this-record--generic",
    },
    {
      branch: "British Army",
      officer: "I do not know",
      destination: Paths.WE_MAY_HOLD_THIS_RECORD,
      template: "we-may-hold-this-record--generic",
    },
    {
      branch: "Royal Air Force",
      officer: "Yes",
      destination: Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__RAF,
      template: "unlikely-to-hold--raf-officer-records",
    },
    {
      branch: "Other",
      officer: "Yes",
      destination: Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__GENERIC,
      template: "we-are-unlikely-to-hold-this-record--generic",
    },
    {
      branch: "I do not know",
      officer: "Yes",
      destination: Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__GENERIC,
      template: "we-are-unlikely-to-hold-this-record--generic",
    },
  ];

  for (const { branch, officer, destination, template } of unchangedJourneys) {
    test(`${branch} with officer answer '${officer}' keeps its existing destination`, async ({
      page,
    }) => {
      await continueFromWhichMilitaryBranchDidThePersonServeIn(page, branch);
      await continueFromWereTheyACommissionedOfficer(
        page,
        officer,
        destination,
        template,
      );
    });
  }
});
