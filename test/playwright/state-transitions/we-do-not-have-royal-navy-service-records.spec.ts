import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  checkExternalLink,
  clickBackLink,
  clickCancelThisRequest,
  continueFromWeDoNotHaveRoyalNavyServiceRecords,
} from "../lib/step-functions";

test.describe("the 'We do not hold this record' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS);
  });

  test("works as expected", async ({ page }) => {
    await continueFromWeDoNotHaveRoyalNavyServiceRecords(page);
  });

  test("checking the external link", async ({ page }) => {
    await checkExternalLink(
      page,
      "Request from the Ministry of Defence",
      "https://www.gov.uk/get-copy-military-records-of-service/apply-for-the-records-of-a-deceased-serviceperson",
    );
  });

  test("clicking the 'Back' link takes the user to 'Which military branch did the person serve in?'", async ({
    page,
  }) => {
    await clickBackLink(
      page,
      Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN,
    );
  });

  test("clicking the 'Back' link on 'Are you sure you want to cancel? page brings the user back'", async ({
    page,
  }) => {
    await clickCancelThisRequest(page, "button");
    await clickBackLink(page, Paths.WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS);
  });

  test("clicking the 'No' link on 'Are you sure you want to cancel? page brings the user back'", async ({
    page,
  }) => {
    await clickCancelThisRequest(page, "button");
    await page.locator("form#cancel-request a").click();
    await expect(page).toHaveURL(
      Paths.WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS,
    );
  });
});
