import { test, expect } from "@playwright/test";

test.describe("the 'Were they a commissioned officer?' form", () => {
  const basePath = "/request-a-service-record";

  enum Urls {
    JOURNEY_START_PAGE = `${basePath}/start/`,
    WAS_SERVICE_PERSON_AN_OFFICER = `${basePath}/was-service-person-officer/`,
    WE_DO_NOT_HAVE_RECORDS_FOR_THIS_RANK = `${basePath}/we-do-not-have-records-for-this-rank/`,
    WE_MAY_HOLD_THIS_RECORD = `${basePath}/we-may-hold-this-record/`,
  }

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.JOURNEY_START_PAGE); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Urls.WAS_SERVICE_PERSON_AN_OFFICER);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /Were they a commissioned officer\?/,
    );
  });

  test.describe("when submitted", () => {
    test("without a submission, shows an error", async ({ page }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-form__error-message")).toHaveText(
        /Choosing an option is required/,
      );
    });

    const selectionMappings = [
      {
        branchLabel: "Yes",
        nextUrl: Urls.WE_DO_NOT_HAVE_RECORDS_FOR_THIS_RANK,
        heading: /We do not have records for this rank/,
        description:
          "when 'Yes' is selected, presents the 'We do not have records for this rank' page ",
      },
      {
        branchLabel: "No",
        nextUrl: Urls.WE_MAY_HOLD_THIS_RECORD,
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
          await page.goto(Urls.JOURNEY_START_PAGE);
          await page.goto(Urls.WAS_SERVICE_PERSON_AN_OFFICER);
          await page.getByLabel(branchLabel, { exact: true }).check();
          await page.getByRole("button", { name: /Continue/i }).click();
          await expect(page).toHaveURL(nextUrl);
          const backLink = page.getByRole("link", { name: "Back" });
          // If there's a "Back" link, click it
          if ((await backLink.count()) > 0) {
            await backLink.click();
            await expect(page).toHaveURL(Urls.WAS_SERVICE_PERSON_AN_OFFICER);
            await expect(
              page.getByLabel(branchLabel, { exact: true }),
            ).toBeChecked();
          }
        });
      });
    });
  });
});
