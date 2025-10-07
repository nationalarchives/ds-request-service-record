import { test, expect } from "@playwright/test";

test.describe("the 'Is the person still alive?' form", () => {
  const basePath = "/request-a-service-record";

  enum Urls {
    JOURNEY_START_PAGE = `${basePath}/start/`,
    IS_SERVICE_PERSON_ALIVE = `${basePath}/is-service-person-alive/`,
    MUST_SUBMIT_SUBJECT_ACCESS = `${basePath}/must-submit-subject-access/`,
    SELECT_SERVICE_BRANCH = `${basePath}/service-branch/`,
    ONLY_LIVING_SUBJECTS_CAN_REQUEST_THEIR_OWN_RECORD = `${basePath}/only-living-subjects-can-request-their-record/`,
    HAVE_YOU_CHECKED_THE_CATALOGUE = `${basePath}/have-you-checked-the-catalogue/`,
  }

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.JOURNEY_START_PAGE); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Urls.IS_SERVICE_PERSON_ALIVE);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /Is the service person still alive\?/,
    );
  });

  test.describe("when submitted", () => {
    test("without a submission, shows an error", async ({ page }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-fieldset__error")).toHaveText(
        /An answer to this question is required/,
      );
    });
  });

  const selectionMappings = [
    {
      label: "Yes",
      url: Urls.MUST_SUBMIT_SUBJECT_ACCESS,
      heading: /Submit a data request for a living subject/,
      description:
        "when 'Yes' is selected, presents the 'Data request for a living person' page ",
    },
    {
      label: "No",
      url: Urls.SELECT_SERVICE_BRANCH,
      heading: /What was the person's service branch\?/,
      description: "when 'No' is selected, presents the 'Service branch' form",
    },
  ];

  selectionMappings.forEach(({ label, url, heading, description }) => {
    test(description, async ({ page }) => {
      await page.getByLabel(label, { exact: true }).check();
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(url);
      await expect(page.locator("h1")).toHaveText(heading);
    });
  });

  test.describe("clicking the 'Back' link after a submission", () => {
    selectionMappings.forEach(({ label, url, heading }) => {
      test(`when '${label}' was submitted, '${label}' is presented when the user returns`, async ({
        page,
      }) => {
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

  test("clicking the 'Back' link takes the user to the 'Have you checked the catalogue? page'", async ({
    page,
  }) => {
    await page.getByRole("link", { name: "Back" }).click();
    await expect(page).toHaveURL(Urls.HAVE_YOU_CHECKED_THE_CATALOGUE);
  });
});
