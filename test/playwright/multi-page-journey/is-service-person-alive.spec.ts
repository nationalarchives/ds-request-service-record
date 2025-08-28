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

  test("Presents the 'Data request for a living person' page when 'Yes' is selected", async ({
    page,
  }) => {
    await page.getByLabel("Yes").check();
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page).toHaveURL(Urls.MUST_SUBMIT_SUBJECT_ACCESS);
    await expect(page.locator("h1")).toHaveText(
      /Submit a data request for a living subject/,
    );
  });

  test("Presents the 'Service branch' form when 'No' is selected", async ({
    page,
  }) => {
    await page.getByLabel("No", { exact: true }).check();
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page).toHaveURL(Urls.SELECT_SERVICE_BRANCH);
    await expect(page.locator("h1")).toHaveText(
      /What was the person's service branch\?/,
    );
  });

  test("Presents the page explaining records for living persons can only be released to themselves when 'I don't know' is selected", async ({
    page,
  }) => {
    await page.getByLabel("I don't know", { exact: true }).check();
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page).toHaveURL(
      Urls.ONLY_LIVING_SUBJECTS_CAN_REQUEST_THEIR_OWN_RECORD,
    );
    await expect(page.locator("h1")).toHaveText(
      /Service records of living persons can only be released to themselves/,
    );
  });
});
