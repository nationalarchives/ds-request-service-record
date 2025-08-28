import { test, expect } from "@playwright/test";

test.describe("What was the person's service branch?", () => {
  const JOURNEY_START_PAGE_URL = "/request-a-service-record/start/";
  const SERVICE_BRANCH_URL = "/request-a-service-record/service-branch/";
  const WAS_SERVICE_PERSON_OFFICER_URL =
    "/request-a-service-record/was-service-person-officer/";
  const MOD_HAVE_THIS_RECORD_URL = "/request-a-service-record/mod-have-this-record/";
  const CHECK_ANCESTRY_URL = "/request-a-service-record/check-ancestry/";

  test.beforeEach(async ({ page }) => {
    await page.goto(JOURNEY_START_PAGE_URL); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(SERVICE_BRANCH_URL);
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
      nextUrl: WAS_SERVICE_PERSON_OFFICER_URL,
      expectedHeading: /Was the service person an officer\?/,
    },
    {
      branchLabel: "Royal Navy",
      nextUrl: MOD_HAVE_THIS_RECORD_URL,
      expectedHeading: /The Ministry of Defence has this record/,
    },
    {
      branchLabel: "Royal Air Force",
      nextUrl: WAS_SERVICE_PERSON_OFFICER_URL,
      expectedHeading: /Was the service person an officer\?/,
    },
    {
      branchLabel: "I don't know",
      nextUrl: WAS_SERVICE_PERSON_OFFICER_URL,
      expectedHeading: /Was the service person an officer\?/,
    },
    {
      branchLabel: "Home Guard",
      nextUrl: CHECK_ANCESTRY_URL,
      expectedHeading: /Check Ancestry/,
    },
  ].forEach(({ branchLabel, nextUrl, expectedHeading }) => {
    test(`Presents the correct form when ${branchLabel} is selected`, async ({
      page,
    }) => {
      await page.goto(JOURNEY_START_PAGE_URL);
      await page.goto(SERVICE_BRANCH_URL);
      await page.getByLabel(branchLabel, { exact: true }).check();
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(nextUrl);
      await expect(page.locator("h1")).toHaveText(expectedHeading);
    });
  });
});
