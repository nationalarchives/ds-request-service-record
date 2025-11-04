import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'Were they a commissioned officer?' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Paths.WERE_THEY_A_COMMISSIONED_OFFICER);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /Were they a commissioned officer\?/,
    );
  });

  test.describe("when submitted", () => {
    test("without a submission, shows an error", async ({ page }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-fieldset__error")).toHaveText(
        /Choosing an option is required/,
      );
    });

    const selectionMappings = [
      {
        branchLabel: "Yes",
        nextUrl: Paths.WE_DO_NOT_HAVE_RECORDS_FOR_THIS_RANK,
        heading: /We do not have records for this rank/,
        description:
          "when 'Yes' is selected, presents the 'We do not have records for this rank' page ",
      },
      {
        branchLabel: "No",
        nextUrl: Paths.WE_MAY_HOLD_THIS_RECORD,
        heading: /We may hold this record/,
        description:
          "when 'No' is selected, presents the 'We may hold this record' page ",
      },
    ];

    selectionMappings.forEach(
      ({ branchLabel, nextUrl, heading, description }) => {
        test(description, async ({ page }) => {
          await page.getByLabel(branchLabel, { exact: true }).check();
          await page.getByRole("button", { name: /Continue/i }).click();
          await expect(page).toHaveURL(nextUrl);
          await expect(page.locator("h1")).toHaveText(heading);
        });
      },
    );

    test.describe("when the 'back' link is clicked, the user's previous selection is shown", () => {
      selectionMappings.forEach(({ branchLabel, nextUrl }) => {
        test(`when ${branchLabel} had been submitted, ${branchLabel} is selected when the 'Back' link is clicked`, async ({
          page,
        }) => {
          await page.goto(Paths.JOURNEY_START);
          await page.goto(Paths.WERE_THEY_A_COMMISSIONED_OFFICER);
          await page.getByLabel(branchLabel, { exact: true }).check();
          await page.getByRole("button", { name: /Continue/i }).click();
          await expect(page).toHaveURL(nextUrl);
          const backLink = page.getByRole("link", { name: "Back" });
          // If there's a "Back" link, click it
          if ((await backLink.count()) > 0) {
            await backLink.click();
            await expect(page).toHaveURL(
              Paths.WERE_THEY_A_COMMISSIONED_OFFICER,
            );
            await expect(
              page.getByLabel(branchLabel, { exact: true }),
            ).toBeChecked();
          }
        });
      });
    });
  });
});
