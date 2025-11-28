import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

// This test suite is a little different to others because we must select the service branch
// before making a selection about whether they were a commissioned officer. This is because
// the page a user is routed to will depend on the combination of these two inputs

test.describe("combinations of 'Which military branch' and 'Were they an officer'", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Paths.SELECT_SERVICE_BRANCH);
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
    ];

    selectionMappings.forEach(
      ({
        serviceBranchLabel,
        officerLabel,
        nextUrl,
        expectedHeading,
        expectedTemplateIdentifier,
      }) => {
        test(`when '${serviceBranchLabel}' is selected for service branch AND '${officerLabel}' is selected for commissioned officer, the user is taken to ${nextUrl}`, async ({
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
        });
      },
    );
  });

  //
  // test.describe("when submitted", () => {
  //   test("without a submission, shows an error", async ({ page }) => {
  //     await page.getByRole("button", { name: /Continue/i }).click();
  //     await expect(page.locator(".tna-fieldset__error")).toHaveText(
  //       /Tell us if the service person was a commissioned officer/,
  //     );
  //   });
  //
  //   const selectionMappings = [
  //     {
  //       branchLabel: "Yes",
  //       nextUrl: Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY,
  //       heading: /We are unlikely to hold this record/,
  //       description:
  //         "when 'Yes' is selected, presents the 'We are unlikely to hold this record' page ",
  //     },
  //     {
  //       branchLabel: "No",
  //       nextUrl: Paths.WE_MAY_HOLD_THIS_RECORD,
  //       heading: /We may hold this record/,
  //       description:
  //         "when 'No' is selected, presents the 'We may hold this record' page ",
  //     },
  //   ];
  //
  //   selectionMappings.forEach(
  //     ({ branchLabel, nextUrl, heading, description }) => {
  //       test(description, async ({ page }) => {
  //         await page.getByLabel(branchLabel, { exact: true }).check();
  //         await page.getByRole("button", { name: /Continue/i }).click();
  //         await expect(page).toHaveURL(nextUrl);
  //         await expect(page.locator("h1")).toHaveText(heading);
  //       });
  //     },
  //   );
  //
  //   test.describe("when the 'back' link is clicked, the user's previous selection is shown", () => {
  //     selectionMappings.forEach(({ branchLabel, nextUrl }) => {
  //       test(`when ${branchLabel} had been submitted, ${branchLabel} is selected when the 'Back' link is clicked`, async ({
  //         page,
  //       }) => {
  //         await page.goto(Paths.JOURNEY_START);
  //         await page.goto(Paths.WERE_THEY_A_COMMISSIONED_OFFICER);
  //         await page.getByLabel(branchLabel, { exact: true }).check();
  //         await page.getByRole("button", { name: /Continue/i }).click();
  //         await expect(page).toHaveURL(nextUrl);
  //         const backLink = page.getByRole("link", { name: "Back" });
  //         // If there's a "Back" link, click it
  //         if ((await backLink.count()) > 0) {
  //           await backLink.click();
  //           await expect(page).toHaveURL(
  //             Paths.WERE_THEY_A_COMMISSIONED_OFFICER,
  //           );
  //           await expect(
  //             page.getByLabel(branchLabel, { exact: true }),
  //           ).toBeChecked();
  //         }
  //       });
  //     });
  //   });
  // });
});
