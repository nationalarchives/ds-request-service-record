import { test, expect } from "@playwright/test";

test.describe("is this person still alive", () => {
  const basePath = "/request-a-service-record";

  enum Urls {
    JOURNEY_START_PAGE = `${basePath}/start/`,
    IS_SERVICE_PERSON_ALIVE = `${basePath}/is-service-person-alive/`,
    MUST_SUBMIT_SUBJECT_ACCESS = `${basePath}/must-submit-subject-access/`,
    SELECT_SERVICE_BRANCH = `${basePath}/service-branch/`,
    ONLY_LIVING_SUBJECTS_CAN_REQUEST_THEIR_OWN_RECORD = `${basePath}/only-living-subjects-can-request-their-record/`,
  }

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.JOURNEY_START_PAGE); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Urls.IS_SERVICE_PERSON_ALIVE);
  });

  test("Shows the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/Is this person still alive\?/);
  });

  test("Shows an error if no option is selected and the user clicks 'Continue'", async ({
    page,
  }) => {
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page.locator(".tna-form__error-message")).toHaveText(
      /An answer to this question is required/,
    );
  });

  const selectionMappings = [
    {
      label: "Yes",
      url: Urls.MUST_SUBMIT_SUBJECT_ACCESS,
      heading: /Submit a data request for a living subject/,
      description:
        "Presents the 'Data request for a living person' page when 'Yes' is selected",
    },
    {
      label: "No",
      url: Urls.SELECT_SERVICE_BRANCH,
      heading: /What was the person's service branch\?/,
      description: "Presents the 'Service branch' form when 'No' is selected",
    },
    {
      label: "I don't know",
      url: Urls.ONLY_LIVING_SUBJECTS_CAN_REQUEST_THEIR_OWN_RECORD,
      heading:
        /Service records of living persons can only be released to themselves/,
      description:
        "Presents the page explaining records for living persons can only be released to themselves when 'I don't know' is selected",
    },
  ];

  test.describe("Selecting an option and clicking 'Continue'", () => {
    selectionMappings.forEach(({ label, url, heading, description }) => {
      test(description, async ({ page }) => {
        await page.getByLabel(label, { exact: true }).check();
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(url);
        await expect(page.locator("h1")).toHaveText(heading);
      });
    });
  });

  test.describe("Having submitted a selection, clicking the 'Back' link ", () => {
    selectionMappings.forEach(({ label, url, heading, description }) => {
      test(description, async ({ page }) => {
        await page.getByLabel(label, { exact: true }).check();
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(url);
        await expect(page.locator("h1")).toHaveText(heading);
        await page.getByRole("link", { name: "Back" }).click();
        await expect(page).toHaveURL(Urls.IS_SERVICE_PERSON_ALIVE);
        await expect(page.getByLabel(label, { exact: true })).toBeChecked();
      });
    });
  });

  test("clicking the 'Back' link takes the user to the start of the journey", async ({
    page,
  }) => {
    await page.getByRole("link", { name: "Back" }).click();
    await expect(page).toHaveURL(Urls.JOURNEY_START_PAGE);
  });
});
