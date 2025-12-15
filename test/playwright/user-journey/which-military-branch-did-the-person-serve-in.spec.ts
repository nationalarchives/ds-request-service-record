import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the service branch form", () => {
  const selectionMappings = [
    {
      branchLabel: "British Army",
      nextUrl: Paths.WERE_THEY_A_COMMISSIONED_OFFICER,
      expectedHeading: /Were they a commissioned officer\?/,
    },
    {
      branchLabel: "Royal Navy (including Royal Marines)",
      nextUrl: Paths.WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS,
      expectedHeading: /We do not hold this record/,
    },
    {
      branchLabel: "Royal Air Force",
      nextUrl: Paths.WERE_THEY_A_COMMISSIONED_OFFICER,
      expectedHeading: /Were they a commissioned officer\?/,
    },
    {
      branchLabel: "I do not know",
      nextUrl: Paths.WERE_THEY_A_COMMISSIONED_OFFICER,
      expectedHeading: /Were they a commissioned officer\?/,
    },
    {
      branchLabel: "Home Guard",
      nextUrl: Paths.WE_ARE_UNLIKELY_TO_LOCATE_THIS_RECORD,
      expectedHeading: /We are unlikely to be able to locate this record/,
    },
  ];

  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Paths.IS_SERVICE_PERSON_ALIVE);
    await page.goto(Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN);
  });

  test.describe("when first rendered", () => {
    test("has the correct heading", async ({ page }) => {
      await expect(page.locator("h1")).toHaveText(
        /Which military branch did the person serve in\?/,
      );
    });
  });

  test.describe("when interacted with", () => {
    test("clicking the 'Back' link takes the user to the 'Is the service person alive? page'", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Paths.IS_SERVICE_PERSON_ALIVE);
    });

    test("submitting without a selection, shows a validation error", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-fieldset__error")).toHaveText(
        /Select the branch they served in/,
      );
    });
    selectionMappings.forEach(({ branchLabel, nextUrl, expectedHeading }) => {
      test(`when ${branchLabel} is submitted, the user is taken to ${nextUrl}`, async ({
        page,
      }) => {
        await page.goto(Paths.JOURNEY_START);
        await page.goto(Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN);
        await page.getByLabel(branchLabel, { exact: true }).check();
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(nextUrl);
        await expect(page.locator("h1")).toHaveText(expectedHeading);
      });
    });

    test.describe("after submission, when the 'back' link is clicked, the user's previous selection is maintained", () => {
      selectionMappings.forEach(({ branchLabel, nextUrl }) => {
        test(`when ${branchLabel} had been submitted, ${branchLabel} is selected when the 'Back' link is clicked`, async ({
          page,
        }) => {
          await page.goto(Paths.JOURNEY_START);
          await page.goto(Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN);
          await page.getByLabel(branchLabel, { exact: true }).check();
          await page.getByRole("button", { name: /Continue/i }).click();
          await expect(page).toHaveURL(nextUrl);
          await page.getByRole("link", { name: "Back" }).click();
          await expect(page).toHaveURL(
            Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN,
          );
          await expect(
            page.getByLabel(branchLabel, { exact: true }),
          ).toBeChecked();
        });
      });
    });
  });
});
