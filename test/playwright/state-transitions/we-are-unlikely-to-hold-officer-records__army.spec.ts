import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  checkExternalLink,
  checkInternalLink,
  clickBackLink,
  clickCancelThisRequest,
  continueFromWeAreUnlikelyToHoldThisRecord,
} from "../lib/step-functions";

test.describe("The variant of 'We are unlikely to hold this record' for Army Officers", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY);
  });

  test("tells users that Full record check is the only order option", async ({
    page,
  }) => {
    await expect(page.locator("main")).toHaveText(
      /These records can only be requested from us using a Full record check/,
    );
  });

  test("works as expected", async ({ page }) => {
    await continueFromWeAreUnlikelyToHoldThisRecord(
      page,
      Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY,
    );
  });

  test("presents the correct exceptions to the rule", async ({ page }) => {
    const exceptions = [/Welsh Guards/, /Grenadier Guards/];
    const exceptionsList = page.locator("#exceptions-list");
    await Promise.all(
      exceptions.map((exception) =>
        expect(exceptionsList).toContainText(exception),
      ),
    );
  });

  test.describe("when interacted with", () => {
    test('clicking "Back" takes the user back to the "Were they a commissioned officer?" page', async ({
      page,
    }) => {
      await clickBackLink(page, Paths.WERE_THEY_A_COMMISSIONED_OFFICER);
    });
    test("once on 'What was their date of birth?' page, clicking 'Back' brings the user back", async ({
      page,
    }) => {
      await continueFromWeAreUnlikelyToHoldThisRecord(
        page,
        Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY,
      );
      await clickBackLink(
        page,
        Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY,
      );
    });
  });

  test.describe("when clicking 'Cancel this request'", () => {
    test("takes the user to the 'Are you sure you want to cancel?' page", async ({
      page,
    }) => {
      await clickCancelThisRequest(page, "link");
    });

    test.describe("then", () => {
      test("clicking 'Back' from 'Are you sure you want to cancel?' brings the user back", async ({
        page,
      }) => {
        await clickCancelThisRequest(page, "link");
        await clickBackLink(
          page,
          Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY,
        );
      });

      test("clicking 'No' from 'Are you sure you want to cancel?' brings the user back", async ({
        page,
      }) => {
        await clickCancelThisRequest(page, "link");
        await page.getByRole("link", { name: "No", exact: true }).click();
        await expect(page).toHaveURL(
          Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY,
        );
      });
    });
  });
});
