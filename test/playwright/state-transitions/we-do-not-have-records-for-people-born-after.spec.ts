import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  checkExternalLink,
  clickBackLink,
  continueFromWeDoNotHaveRecordsForPeopleBornAfter,
} from "../lib/step-functions";

test.describe("The 'We do not have records for people born after 1939' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.WE_DO_NOT_HAVE_RECORDS_FOR_PEOPLE_BORN_AFTER);
  });

  test("works as expected", async ({ page }) => {
    await continueFromWeDoNotHaveRecordsForPeopleBornAfter(page);
  });

  test("checking the external link", async ({ page }) => {
    await checkExternalLink(
      page,
      "Request from the Ministry of Defence",
      "https://www.gov.uk/get-copy-military-records-of-service/apply-for-the-records-of-a-deceased-serviceperson",
    );
  });

  test("clicking the 'Back' link takes the user to 'What was their date of birth?'", async ({
    page,
  }) => {
    await clickBackLink(page, Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH);
  });

  test("clicking the 'Back' link on 'Are you sure you want to cancel? page brings the user back'", async ({
    page,
  }) => {
    await continueFromWeDoNotHaveRecordsForPeopleBornAfter(page);
    await clickBackLink(
      page,
      Paths.WE_DO_NOT_HAVE_RECORDS_FOR_PEOPLE_BORN_AFTER,
    );
  });
});
