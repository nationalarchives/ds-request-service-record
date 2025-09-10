import { test, expect } from "@playwright/test";

test.describe("the 'What was the person's service branch?' form", () => {
  const basePath = "/request-a-service-record";

  enum Urls {
    JOURNEY_START_PAGE = `${basePath}/start/`,
    SERVICE_BRANCH = `${basePath}/service-branch/`,
    WAS_SERVICE_PERSON_AN_OFFICER = `${basePath}/was-service-person-officer/`,
    WE_DO_NOT_HAVE_THIS_RECORD = `${basePath}/we-do-not-have-this-record/`,
    WE_MAY_BE_UNABLE_TO_FIND_THIS_RECORD = `${basePath}/we-may-be-unable-to-find-this-record/`,
  }

  const selectionMappings = [
    {
      branchLabel: "British Army",
      nextUrl: Urls.WAS_SERVICE_PERSON_AN_OFFICER,
      expectedHeading: /Were they a commissioned officer\?/,
      destinationPageHasBackLink: true,
    },
    {
      branchLabel: "Royal Navy",
      nextUrl: Urls.WE_DO_NOT_HAVE_THIS_RECORD,
      expectedHeading: /We do not have this record/,
      destinationPageHasBackLink: false,
    },
    {
      branchLabel: "Royal Air Force",
      nextUrl: Urls.WAS_SERVICE_PERSON_AN_OFFICER,
      expectedHeading: /Were they a commissioned officer\?/,
      destinationPageHasBackLink: true,
    },
    {
      branchLabel: "I don't know",
      nextUrl: Urls.WAS_SERVICE_PERSON_AN_OFFICER,
      expectedHeading: /Were they a commissioned officer\?/,
      destinationPageHasBackLink: true,
    },
    {
      branchLabel: "Home Guard",
      nextUrl: Urls.WE_MAY_BE_UNABLE_TO_FIND_THIS_RECORD,
      expectedHeading: /We may have this record/,
      destinationPageHasBackLink: false,
    },
  ];

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.JOURNEY_START_PAGE); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Urls.SERVICE_BRANCH);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /What was the person's service branch\?/,
    );
  });

  test.describe("when submitted", () => {
    test("without a selection, keeps the user on the page and shows a validation error", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-form__error-message")).toHaveText(
        /The service person's service branch is required/,
      );
    });
    selectionMappings.forEach(({ branchLabel, nextUrl, expectedHeading }) => {
      test(`when ${branchLabel} is submitted, the user is taken to ${nextUrl}`, async ({
        page,
      }) => {
        await page.goto(Urls.JOURNEY_START_PAGE);
        await page.goto(Urls.SERVICE_BRANCH);
        await page.getByLabel(branchLabel, { exact: true }).check();
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(nextUrl);
        await expect(page.locator("h1")).toHaveText(expectedHeading);
      });
    });

    test.describe("when the 'back' link is clicked, the user's previous selection is shown", () => {
      selectionMappings.forEach(
        ({ branchLabel, nextUrl, destinationPageHasBackLink }) => {
          if (!destinationPageHasBackLink) {
            return; // Skip this iteration if the destination page does not have a back link
          }
          test(`when ${branchLabel} had been submitted, ${branchLabel} is selected when the 'Back' link is clicked`, async ({
            page,
          }) => {
            await page.goto(Urls.JOURNEY_START_PAGE);
            await page.goto(Urls.SERVICE_BRANCH);
            await page.getByLabel(branchLabel, { exact: true }).check();
            await page.getByRole("button", { name: /Continue/i }).click();
            await expect(page).toHaveURL(nextUrl);
            await page.getByRole("link", { name: "Back" }).click();
            await expect(page).toHaveURL(Urls.SERVICE_BRANCH);
            await expect(
              page.getByLabel(branchLabel, { exact: true }),
            ).toBeChecked();
          });
        },
      );
    });
  });
});
