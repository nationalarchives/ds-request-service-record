import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

// This test suite is a little different to others because it covers multiple pages:
// we must select the service branch, then we must select whether they were an officer.
// This is because the page a user is routed to will depend on the combination of these two inputs

test.describe("combinations of 'Which military branch' and 'Were they an officer'", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN);
  });

  test("when selecting the military branch, we present the correct heading", async ({
    page,
  }) => {
    await expect(page.locator("h1")).toHaveText(
      /Which military branch did the person serve in\?/,
    );
  });

  test.describe("when service branch and officer status is selected", () => {
    const selectionMappings = [
      {
        serviceBranchLabel: "British Army",
        officerLabel: "Yes",
        nextUrl: Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY,
        expectedHeading: /We are unlikely to hold this record/,
        expectedTemplateIdentifier: "unlikely-to-hold--army-officer-records",
      },
      {
        serviceBranchLabel: "British Army",
        officerLabel: "No",
        nextUrl: Paths.WE_MAY_HOLD_THIS_RECORD,
        expectedHeading: /We may hold this record/,
        expectedTemplateIdentifier: "we-may-hold-this-record--generic",
      },
      {
        serviceBranchLabel: "British Army",
        officerLabel: "I do not know",
        nextUrl: Paths.WE_MAY_HOLD_THIS_RECORD,
        expectedHeading: /We may hold this record/,
        expectedTemplateIdentifier: "we-may-hold-this-record--generic",
      },
      {
        serviceBranchLabel: "Royal Air Force",
        officerLabel: "Yes",
        nextUrl: Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__RAF,
        expectedHeading: /We are unlikely to hold this record/,
        expectedTemplateIdentifier: "unlikely-to-hold--raf-officer-records",
      },
      {
        serviceBranchLabel: "Royal Air Force",
        officerLabel: "No",
        nextUrl: Paths.WE_MAY_HOLD_THIS_RECORD,
        expectedHeading: /We may hold this record/,
        expectedTemplateIdentifier: "we-may-hold-this-record--generic",
      },
      {
        serviceBranchLabel: "Royal Air Force",
        officerLabel: "I do not know",
        nextUrl: Paths.WE_MAY_HOLD_THIS_RECORD,
        expectedHeading: /We may hold this record/,
        expectedTemplateIdentifier: "we-may-hold-this-record--generic",
      },
      {
        serviceBranchLabel: "Other",
        officerLabel: "Yes",
        nextUrl: Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__GENERIC,
        expectedHeading: /We are unlikely to hold this record/,
        expectedTemplateIdentifier:
          "we-are-unlikely-to-hold-this-record--generic",
      },
      {
        serviceBranchLabel: "Other",
        officerLabel: "No",
        nextUrl: Paths.WE_MAY_HOLD_THIS_RECORD,
        expectedHeading: /We may hold this record/,
        expectedTemplateIdentifier: "we-may-hold-this-record--generic",
      },
      {
        serviceBranchLabel: "Other",
        officerLabel: "I do not know",
        nextUrl: Paths.WE_MAY_HOLD_THIS_RECORD,
        expectedHeading: /We may hold this record/,
        expectedTemplateIdentifier: "we-may-hold-this-record--generic",
      },
      {
        serviceBranchLabel: "I do not know",
        officerLabel: "Yes",
        nextUrl: Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__GENERIC,
        expectedHeading: /We are unlikely to hold this record/,
        expectedTemplateIdentifier:
          "we-are-unlikely-to-hold-this-record--generic",
      },
      {
        serviceBranchLabel: "I do not know",
        officerLabel: "No",
        nextUrl: Paths.WE_MAY_HOLD_THIS_RECORD,
        expectedHeading: /We may hold this record/,
        expectedTemplateIdentifier: "we-may-hold-this-record--generic",
      },
      {
        serviceBranchLabel: "I do not know",
        officerLabel: "I do not know",
        nextUrl: Paths.WE_MAY_HOLD_THIS_RECORD,
        expectedHeading: /We may hold this record/,
        expectedTemplateIdentifier: "we-may-hold-this-record--generic",
      },
    ];

    selectionMappings.forEach(
      ({
        serviceBranchLabel,
        officerLabel,
        nextUrl,
        expectedHeading,
        expectedTemplateIdentifier,
      }) => {
        test(`when '${serviceBranchLabel}' is selected for service branch AND '${officerLabel}' is selected for commissioned officer, the user is taken to ${nextUrl} and the 'Back' link works as expected`, async ({
          page,
        }) => {
          await page.getByLabel(serviceBranchLabel, { exact: true }).check();
          await page.getByRole("button", { name: /Continue/i }).click();
          await expect(page.locator("h1")).toHaveText(
            /Were they a commissioned officer\?/,
          );
          await page.getByLabel(officerLabel, { exact: true }).check();
          await page.getByRole("button", { name: /Continue/i }).click();
          await expect(page).toHaveURL(nextUrl);
          await expect(page.locator("h1")).toHaveText(expectedHeading);
          // Because the templates in this part of the journey can be only subtly different,
          // we check for a template identifier to ensure the correct template is shown
          await expect(
            page.locator(`[data-template-id="${expectedTemplateIdentifier}"]`),
          ).toBeVisible();
          // Here we are checking that the 'Back' link always takes the user to the correct page
          await page.getByRole("link", { name: "Back" }).click();
          await expect(page).toHaveURL(Paths.WERE_THEY_A_COMMISSIONED_OFFICER);
        });
      },
    );
  });

  test.describe("when submitted", () => {
    test("without a selection, shows an error", async ({ page }) => {
      await page.goto(Paths.WERE_THEY_A_COMMISSIONED_OFFICER);
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-fieldset__error")).toHaveText(
        /Tell us if the service person was a commissioned officer/,
      );
    });
  });
});
