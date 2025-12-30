import { expect, test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  checkExternalLink,
  clickBackLink,
  continueFromWeAreUnlikelyToLocateThisRecord,
} from "../lib/step-functions";

test.describe("the 'We are unlikely to be able to locate this record' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.WE_ARE_UNLIKELY_TO_LOCATE_THIS_RECORD);
  });

  test("works as expected", async ({ page }) => {
    await continueFromWeAreUnlikelyToLocateThisRecord(page);
  });

  test("clicking the 'No' link on 'Are you sure you want to cancel? page brings the user back'", async ({
    page,
  }) => {
    await continueFromWeAreUnlikelyToLocateThisRecord(page);
    await page.locator("form#cancel-request a").click();
    await expect(page).toHaveURL(Paths.WE_ARE_UNLIKELY_TO_LOCATE_THIS_RECORD);
  });

  test("clicking the 'Back' link on the next page brings the user back", async ({
    page,
  }) => {
    await continueFromWeAreUnlikelyToLocateThisRecord(page);
    await clickBackLink(page, Paths.WE_ARE_UNLIKELY_TO_LOCATE_THIS_RECORD);
  });

  test.describe("inspecting the external link", () => {
    test("the 'Request a paid search' link", async ({ page }) => {
      await checkExternalLink(
        page,
        "Request a paid search",
        "https://www.nationalarchives.gov.uk/contact-us/our-paid-search-service/request-a-paid-search/",
      );
    });
  });
});
