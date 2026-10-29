import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  checkExternalLink,
  continueFromProvidingAProofOfDeath,
} from "../lib/step-functions";
import { testfirstBirthYearForClosedRecords } from "../lib/test-first-birth-year-for-closed-records";
import { testfirstBirthYearStandardOrdersRequireProofOfDeath } from "../lib/test-first-birth-year-standard-orders-require-proof-of-death";

test.describe("the 'Providing a proof of death' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.PROVIDING_A_PROOF_OF_DEATH);
  });

  test("works as expected", async ({ page }) => {
    await continueFromProvidingAProofOfDeath(page, Paths.BEFORE_YOU_START);
  });

  test("has the correct value shown for first birth year for closed records", async ({
    page,
  }) => {
    await testfirstBirthYearForClosedRecords(page);
  });

  test("has the correct value shown for first birth year for standard orders requiring proof of death", async ({
    page,
  }) => {
    await testfirstBirthYearStandardOrdersRequireProofOfDeath(page);
  });

  test("clicking the 'Back' link on the next page DOES NOT bring the user back", async ({
    page,
  }) => {
    await continueFromProvidingAProofOfDeath(page, Paths.BEFORE_YOU_START);
    // In this scenario, we do not want the user to come back to the 'Providing a proof of death' page,
    // so we check that the back link takes them to the 'How we process requests' page instead.
    await clickBackLink(page, Paths.HOW_WE_PROCESS_REQUESTS);
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
  });
});
