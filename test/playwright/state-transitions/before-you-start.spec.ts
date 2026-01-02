import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  checkExternalLink,
  continueFromBeforeYouStart,
  clickExitThisForm,
} from "../lib/step-functions";
import { testLastBirthYearForOpenRecords } from "../lib/test-last-birth-year-for-open-records";

test.describe("the 'Before you start' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.BEFORE_YOU_START);
  });

  test("has the correct value shown for last birth year for open records", async ({
    page,
  }) => {
    await testLastBirthYearForOpenRecords(page);
  });

  test("shows an error when the user tries to proceed without confirming they have the mandatory information", async ({
    page,
  }) => {
    await continueFromBeforeYouStart(page, false);
  });

  test("works as expected", async ({ page }) => {
    await continueFromBeforeYouStart(page, true);
  });

  test("clicking the 'Back' link on the next page brings the user back", async ({
    page,
  }) => {
    await continueFromBeforeYouStart(page, true);
    await clickBackLink(page, Paths.BEFORE_YOU_START);
  });

  test.describe("inspecting the external links", () => {
    test("the 'Copies of death certificates' link", async ({ page }) => {
      await checkExternalLink(
        page,
        "Copies of death certificates (opens in new tab)",
        "https://www.gov.uk/order-copy-birth-death-marriage-certificate",
      );
    });

    test("the 'Commonwealth War Graves’' link", async ({ page }) => {
      await checkExternalLink(
        page,
        "Commonwealth War Graves’ (CWG) war dead records (opens in new tab)",
        "https://www.cwgc.org/find-records/find-war-dead/",
      );
    });

    test("the 'Our privacy notice' link", async ({ page }) => {
      await checkExternalLink(
        page,
        "Our privacy notice (opens in new tab)",
        "https://www.nationalarchives.gov.uk/legal/privacy-policy/",
      );
    });
  });

  test.describe("the 'Exit this form' link", () => {
    test("works as expected", async ({ page }) => {
      await clickExitThisForm(page, "link");
    });
    test("having reached 'Are you sure you want to cancel?', clicking 'Back' brings the user back", async ({
      page,
    }) => {
      await clickExitThisForm(page, "link");
      await clickBackLink(page, Paths.BEFORE_YOU_START);
    });
    test("having reached 'Are you sure you want to cancel?', clicking 'No' brings the user back", async ({
      page,
    }) => {
      await clickExitThisForm(page, "link");
      await page.locator("#cancel-request a").click();
      await expect(page).toHaveURL(Paths.BEFORE_YOU_START);
    });
  });
});
