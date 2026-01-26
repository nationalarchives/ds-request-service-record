import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  checkExternalLink,
  continueFromBeforeYouStart,
} from "../lib/step-functions";
import { testfirstBirthYearForClosedRecords } from "../lib/test-first-birth-year-for-closed-records";

test.describe("the 'Before you start' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.BEFORE_YOU_START);
  });

  test("has the correct value shown for last birth year for open records", async ({
    page,
  }) => {
    await testfirstBirthYearForClosedRecords(page);
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
        "A copy of a death certificate (opens in new tab)",
        "https://www.gov.uk/order-copy-birth-death-marriage-certificate",
      );
    });

    test("the 'Commonwealth War Graves' link", async ({ page }) => {
      await checkExternalLink(
        page,
        "A Commonwealth War Graves Commission (CWGC) war dead record (opens in new tab)",
        "https://www.cwgc.org/find-records/find-war-dead/",
      );
    });

    test("the 'Grant of probate' link", async ({ page }) => {
      await checkExternalLink(
        page,
        "Grant of probate (opens in new tab)",
        "https://probatesearch.service.gov.uk/",
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
});
