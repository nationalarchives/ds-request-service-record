import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  checkExternalLink,
  continueFromBeforeYouStart,
  checkInternalLink,
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

  test.describe("inspecting the links", () => {
    test("the 'Providing a proof of death' link", async ({ page }) => {
      await checkInternalLink(
        page,
        "Find out more about proof of death",
        "/request-a-military-service-record/providing-a-proof-of-death/",
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
