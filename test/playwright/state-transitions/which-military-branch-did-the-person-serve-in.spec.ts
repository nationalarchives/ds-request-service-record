import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromWhichMilitaryBranchDidThePersonServeIn,
} from "../lib/step-functions";

test.describe("the service branch form", () => {
  const selectionMappings = [
    {
      branchLabel: "British Army",
      nextUrl: Paths.WERE_THEY_A_COMMISSIONED_OFFICER,
    },
    {
      branchLabel: "Royal Navy (including Royal Marines)",
      nextUrl: Paths.WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS,
    },
    {
      branchLabel: "Royal Air Force",
      nextUrl: Paths.WERE_THEY_A_COMMISSIONED_OFFICER,
    },
    {
      branchLabel: "I do not know",
      nextUrl: Paths.WERE_THEY_A_COMMISSIONED_OFFICER,
    },
    {
      branchLabel: "Home Guard",
      nextUrl: Paths.WE_ARE_UNLIKELY_TO_LOCATE_THIS_RECORD,
    },
  ];

  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN);
  });

  test.describe("when interacted with", () => {
    test("clicking the 'Back' link takes the user to the 'Is the service person alive? page'", async ({
      page,
    }) => {
      await clickBackLink(page, Paths.IS_SERVICE_PERSON_ALIVE);
    });

    test("submitting without a selection, shows a validation error", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-fieldset__error")).toHaveText(
        /Select the branch they served in/,
      );
    });
    selectionMappings.forEach(({ branchLabel, nextUrl }) => {
      test(`when ${branchLabel} is submitted, the user is taken to ${nextUrl}`, async ({
        page,
      }) => {
        await continueFromWhichMilitaryBranchDidThePersonServeIn(
          page,
          branchLabel,
          nextUrl,
        );
      });
    });

    test.describe("after submission, when the 'back' link is clicked, the user's previous selection is maintained", () => {
      selectionMappings.forEach(({ branchLabel, nextUrl }) => {
        test(`when ${branchLabel} had been submitted, ${branchLabel} is selected when the 'Back' link is clicked`, async ({
          page,
        }) => {
          await continueFromWhichMilitaryBranchDidThePersonServeIn(
            page,
            branchLabel,
            nextUrl,
          );
          await clickBackLink(
            page,
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
