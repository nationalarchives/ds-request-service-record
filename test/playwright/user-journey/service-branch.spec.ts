import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'Which military branch did the person serve in?' form", () => {
  const selectionMappings = [
    {
      branchLabel: "British Army",
      nextUrl: Paths.WERE_THEY_A_COMMISSIONED_OFFICER,
      expectedHeading: /Were they a commissioned officer\?/,
    },
    {
      branchLabel: "Royal Navy (including Royal Marines)",
      nextUrl: Paths.WE_DO_NOT_HAVE_RECORDS_FOR_THIS_SERVICE_BRANCH,
      expectedHeading: /We do not hold this record/,
    },
    {
      branchLabel: "Royal Air Force",
      nextUrl: Paths.WERE_THEY_A_COMMISSIONED_OFFICER,
      expectedHeading: /Were they a commissioned officer\?/,
    },
    {
      branchLabel: "Don't know",
      nextUrl: Paths.WERE_THEY_A_COMMISSIONED_OFFICER,
      expectedHeading: /Were they a commissioned officer\?/,
    },
    {
      branchLabel: "Home Guard",
      nextUrl: Paths.WE_ARE_UNLIKELY_TO_FIND_THIS_RECORD,
      expectedHeading: /We are unlikely to be able to locate this record/,
    },
  ];

  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Paths.SERVICE_BRANCH);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /Which military branch did the person serve in\?/,
    );
  });

  test.describe("when submitted", () => {
    test("without a selection, keeps the user on the page and shows a validation error", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-fieldset__error")).toHaveText(
        /The person's service branch is required/,
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
