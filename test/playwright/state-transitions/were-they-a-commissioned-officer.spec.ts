import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  continueFromWhichMilitaryBranchDidThePersonServeIn,
  continueFromWereTheyACommissionedOfficer,
  clickBackLink,
} from "../lib/step-functions";

// This test suite is a little different to others because it covers multiple pages:
// we must select the service branch, then we must select whether they were an officer.
// This is because the next page will depend on the combination of both choices.

test.describe("combinations of 'Which military branch' and 'Were they an officer'", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN);
  });

  const selectionMappings = [
    {
      serviceBranchLabel: "British Army",
      officerLabel: "Yes",
      nextUrlAfterOfficerSelection:
        Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY,
      expectedHeading: /We are unlikely to hold this record/,
      expectedTemplateIdentifier: "unlikely-to-hold--army-officer-records",
    },
    {
      serviceBranchLabel: "British Army",
      officerLabel: "No",
      nextUrlAfterOfficerSelection: Paths.WE_MAY_HOLD_THIS_RECORD,
      expectedHeading: /We may hold this record/,
      expectedTemplateIdentifier: "we-may-hold-this-record--generic",
    },
    {
      serviceBranchLabel: "British Army",
      officerLabel: "I do not know",
      nextUrlAfterOfficerSelection: Paths.WE_MAY_HOLD_THIS_RECORD,
      expectedHeading: /We may hold this record/,
      expectedTemplateIdentifier: "we-may-hold-this-record--generic",
    },
    {
      serviceBranchLabel: "Royal Air Force",
      officerLabel: "Yes",
      nextUrlAfterOfficerSelection:
        Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__RAF,
      expectedHeading: /We are unlikely to hold this record/,
      expectedTemplateIdentifier: "unlikely-to-hold--raf-officer-records",
    },
    {
      serviceBranchLabel: "Royal Air Force",
      officerLabel: "No",
      nextUrlAfterOfficerSelection: Paths.WE_MAY_HOLD_THIS_RECORD,
      expectedHeading: /We may hold this record/,
      expectedTemplateIdentifier: "we-may-hold-this-record--generic",
    },
    {
      serviceBranchLabel: "Royal Air Force",
      officerLabel: "I do not know",
      nextUrlAfterOfficerSelection: Paths.WE_MAY_HOLD_THIS_RECORD,
      expectedHeading: /We may hold this record/,
      expectedTemplateIdentifier: "we-may-hold-this-record--generic",
    },
    {
      serviceBranchLabel: "Other",
      officerLabel: "Yes",
      nextUrlAfterOfficerSelection:
        Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__GENERIC,
      expectedHeading: /We are unlikely to hold this record/,
      expectedTemplateIdentifier:
        "we-are-unlikely-to-hold-this-record--generic",
    },
    {
      serviceBranchLabel: "Other",
      officerLabel: "No",
      nextUrlAfterOfficerSelection: Paths.WE_MAY_HOLD_THIS_RECORD,
      expectedHeading: /We may hold this record/,
      expectedTemplateIdentifier: "we-may-hold-this-record--generic",
    },
    {
      serviceBranchLabel: "Other",
      officerLabel: "I do not know",
      nextUrlAfterOfficerSelection: Paths.WE_MAY_HOLD_THIS_RECORD,
      expectedHeading: /We may hold this record/,
      expectedTemplateIdentifier: "we-may-hold-this-record--generic",
    },
    {
      serviceBranchLabel: "I do not know",
      officerLabel: "Yes",
      nextUrlAfterOfficerSelection:
        Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__GENERIC,
      expectedHeading: /We are unlikely to hold this record/,
      expectedTemplateIdentifier:
        "we-are-unlikely-to-hold-this-record--generic",
    },
    {
      serviceBranchLabel: "I do not know",
      officerLabel: "No",
      nextUrlAfterOfficerSelection: Paths.WE_MAY_HOLD_THIS_RECORD,
      expectedHeading: /We may hold this record/,
      expectedTemplateIdentifier: "we-may-hold-this-record--generic",
    },
    {
      serviceBranchLabel: "I do not know",
      officerLabel: "I do not know",
      nextUrlAfterOfficerSelection: Paths.WE_MAY_HOLD_THIS_RECORD,
      expectedHeading: /We may hold this record/,
      expectedTemplateIdentifier: "we-may-hold-this-record--generic",
    },
  ];

  test.describe("when service branch and officer status are combined", () => {
    selectionMappings.forEach(
      ({
        serviceBranchLabel,
        officerLabel,
        nextUrlAfterOfficerSelection,
        expectedTemplateIdentifier,
      }) => {
        test(`when '${serviceBranchLabel}' is selected for service branch AND '${officerLabel}' is selected for commissioned officer, the user is taken to ${nextUrlAfterOfficerSelection} and the 'Back' link works as expected`, async ({
          page,
        }) => {
          await continueFromWhichMilitaryBranchDidThePersonServeIn(
            page,
            serviceBranchLabel,
          );
          await continueFromWereTheyACommissionedOfficer(
            page,
            officerLabel,
            nextUrlAfterOfficerSelection,
            expectedTemplateIdentifier,
          );
        });
      },
    );
  });

  test.describe("when submitted", () => {
    test("without a selection, shows an error", async ({ page }) => {
      await page.goto(Paths.WERE_THEY_A_COMMISSIONED_OFFICER);
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-fieldset__error")).toHaveText(
        /Tell us if the service person was a Commissioned Officer/,
      );
    });
  });

  test.describe("'Back' links from 'Were they a commissioned officer?' always take the user to 'Which military branch did the person serve in?'", () => {
    const justTheServiceBranchLabels = selectionMappings.map(
      ({ serviceBranchLabel }) => serviceBranchLabel,
    );

    // @ts-ignore
    const uniqueServiceBranchLabels = [...new Set(justTheServiceBranchLabels)];

    uniqueServiceBranchLabels.forEach((serviceBranchLabel) => {
      test(`when '${serviceBranchLabel}' was selected to reach the page, the 'Back' link works as expected`, async ({
        page,
      }) => {
        await continueFromWhichMilitaryBranchDidThePersonServeIn(
          page,
          serviceBranchLabel,
        );
        await clickBackLink(
          page,
          Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN,
        );
      });
    });
  });
});
