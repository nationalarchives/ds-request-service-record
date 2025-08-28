import { test, expect } from "@playwright/test";

test.describe("What was the person's service branch?", () => {
  const basePath = "/request-a-service-record";

  enum Urls {
    JOURNEY_START_PAGE = `${basePath}/start/`,
    SERVICE_BRANCH = `${basePath}/service-branch/`,
    WAS_SERVICE_PERSON_OFFICER = `${basePath}/was-service-person-officer/`,
    MOD_HAVE_THIS_RECORD = `${basePath}/mod-have-this-record/`,
    CHECK_ANCESTRY = `${basePath}/check-ancestry/`,
  }

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.JOURNEY_START_PAGE); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Urls.SERVICE_BRANCH);
  });

  test("Shows the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /What was the person's service branch\?/,
    );
  });

  test("Shows an error if no option is selected and the user clicks 'Continue'", async ({
    page,
  }) => {
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page.locator(".tna-form__error-message")).toHaveText(
      /The service person's service branch is required/,
    );
  });

  [
    {
      branchLabel: "British Army",
      nextUrl: Urls.WAS_SERVICE_PERSON_OFFICER,
      expectedHeading: /Was the service person an officer\?/,
    },
    {
      branchLabel: "Royal Navy",
      nextUrl: Urls.MOD_HAVE_THIS_RECORD,
      expectedHeading: /The Ministry of Defence has this record/,
    },
    {
      branchLabel: "Royal Air Force",
      nextUrl: Urls.WAS_SERVICE_PERSON_OFFICER,
      expectedHeading: /Was the service person an officer\?/,
    },
    {
      branchLabel: "I don't know",
      nextUrl: Urls.WAS_SERVICE_PERSON_OFFICER,
      expectedHeading: /Was the service person an officer\?/,
    },
    {
      branchLabel: "Home Guard",
      nextUrl: Urls.CHECK_ANCESTRY,
      expectedHeading: /Check Ancestry/,
    },
  ].forEach(({ branchLabel, nextUrl, expectedHeading }) => {
    test(`Presents the correct form when ${branchLabel} is selected`, async ({
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
});
