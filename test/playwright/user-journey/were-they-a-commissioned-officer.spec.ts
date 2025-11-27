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

  test.describe("when 'Army' is selected as the service branch", () => {
    const selectionMappings = [
      {
        officerLabel: "Yes",
        nextUrl: Paths.WE_ARE_UNLIKELY_TO_HOLD_ARMY_OFFICER_RECORDS,
        expectedHeading: /We are unlikely to hold this record/,
      },
      {
        officerLabel: "No",
        nextUrl: Paths.WE_MAY_HOLD_THIS_RECORD,
        expectedHeading: /We may hold this record/,
      },
    ];

    selectionMappings.forEach(({ officerLabel, nextUrl, expectedHeading }) => {
      test(`when '${officerLabel}' is selected for commissioned officer, the user is taken to ${nextUrl}`, async ({
        page,
      }) => {
        await page.getByLabel("British Army", { exact: true }).check();
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page.locator("h1")).toHaveText(
          /Were they a commissioned officer\?/,
        );
        await page.getByLabel(officerLabel, { exact: true }).check();
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(nextUrl);
        await expect(page.locator("h1")).toHaveText(expectedHeading);
      });
    });
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
  //       nextUrl: Paths.WE_ARE_UNLIKELY_TO_HOLD_ARMY_OFFICER_RECORDS,
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
