import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'What was the person's service branch?' form", () => {
  const selectionMappings = [
    {
      branchLabel: "British Army",
      nextUrl: Paths.WAS_SERVICE_PERSON_AN_OFFICER,
      expectedHeading: /Were they a commissioned officer\?/,
    },
    {
      branchLabel: "Royal Navy",
      nextUrl: Paths.WE_DO_NOT_HAVE_RECORDS_FOR_THIS_SERVICE_BRANCH,
      expectedHeading: /We do not have records for this service branch/,
    },
    {
      branchLabel: "Royal Air Force",
      nextUrl: Paths.WAS_SERVICE_PERSON_AN_OFFICER,
      expectedHeading: /Were they a commissioned officer\?/,
    },
    {
      branchLabel: "I don't know",
      nextUrl: Paths.WAS_SERVICE_PERSON_AN_OFFICER,
      expectedHeading: /Were they a commissioned officer\?/,
    },
    {
      branchLabel: "Home Guard",
      nextUrl: Paths.WE_MAY_BE_UNABLE_TO_FIND_THIS_RECORD,
      expectedHeading: /We may have this record/,
    },
  ];

  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Paths.SERVICE_BRANCH);
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
      await expect(page.locator(".tna-fieldset__error")).toHaveText(
        /The service person's service branch is required/,
      );
    });
    selectionMappings.forEach(({ branchLabel, nextUrl, expectedHeading }) => {
      test(`when ${branchLabel} is submitted, the user is taken to ${nextUrl}`, async ({
        page,
      }) => {
        await page.goto(Paths.JOURNEY_START);
        await page.goto(Paths.SERVICE_BRANCH);
        await page.getByLabel(branchLabel, { exact: true }).check();
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(nextUrl);
        await expect(page.locator("h1")).toHaveText(expectedHeading);
      });
    });

    test.describe("when the 'back' link is clicked, the user's previous selection is shown", () => {
      selectionMappings.forEach(({ branchLabel, nextUrl }) => {
        test(`when ${branchLabel} had been submitted, ${branchLabel} is selected when the 'Back' link is clicked`, async ({
          page,
        }) => {
          await page.goto(Paths.JOURNEY_START);
          await page.goto(Paths.SERVICE_BRANCH);
          await page.getByLabel(branchLabel, { exact: true }).check();
          await page.getByRole("button", { name: /Continue/i }).click();
          await expect(page).toHaveURL(nextUrl);
          const backLink = page.getByRole("link", { name: "Back" });
          // if there's a "Back" link, click it
          if ((await backLink.count()) > 0) {
            await backLink.click();
            await expect(page).toHaveURL(Paths.SERVICE_BRANCH);
            await expect(
              page.getByLabel(branchLabel, { exact: true }),
            ).toBeChecked();
          }
        });
      });
    });
  });
});
