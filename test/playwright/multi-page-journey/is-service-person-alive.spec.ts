import { test, expect } from "@playwright/test";

test.describe("is this person still alive", () => {
  const JOURNEY_START_PAGE_URL = "/request-a-service-record/start/";
  const IS_SERVICE_PERSON_ALIVE_URL =
    "/request-a-service-record/is-service-person-alive/";
  const MUST_SUBMIT_SUBJECT_ACCESS_URL =
    "/request-a-service-record/must-submit-subject-access/";
  const SELECT_SERVICE_BRANCH_URL = "/request-a-service-record/service-branch/";

  test.beforeEach(async ({ page }) => {
    await page.goto(JOURNEY_START_PAGE_URL); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(IS_SERVICE_PERSON_ALIVE_URL);
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
    await expect(page).toHaveURL(MUST_SUBMIT_SUBJECT_ACCESS_URL);
    await expect(page.locator("h1")).toHaveText(
      /Submit a data request for a living subject/,
    );
  });

  test("Presents the 'Service branch' form when 'No' is selected", async ({
    page,
  }) => {
    await page.getByLabel("No").check();
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page).toHaveURL(SELECT_SERVICE_BRANCH_URL);
    await expect(page.locator("h1")).toHaveText(
      /What was the person's service branch\?/,
    );
  });
});
