import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  checkExternalLink,
  clickBackLink,
  clickCancelThisRequest,
  continueFromSubmitDataAccessRequest,
} from "../lib/step-functions";

test.describe("the 'Submit a data access request' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.MUST_SUBMIT_SUBJECT_ACCESS);
  });

  test("works as expected", async ({ page }) => {
    await continueFromSubmitDataAccessRequest(page);
  });

  test("the 'Submit a data access request' link has the correct destination and is set to open in new tab", async ({
    page,
  }) => {
    await checkExternalLink(
      page,
      "Submit a data access request",
      "https://discovery.nationalarchives.gov.uk/mod-dsa-request-step1",
    );
  });

  test.describe("'Cancel this request' and 'Back' links", () => {
    test("clicking the 'Cancel this request' button takes the user to 'Are you sure you want to cancel?'", async ({
      page,
    }) => {
      await clickCancelThisRequest(page, "button");
    });

    test("clicking the 'Back' link on 'Are you sure you want to cancel? page brings the user back'", async ({
      page,
    }) => {
      await clickCancelThisRequest(page, "button");
      await clickBackLink(page, Paths.MUST_SUBMIT_SUBJECT_ACCESS);
    });

    test("clicking the 'No' link on 'Are you sure you want to cancel? page brings the user back'", async ({
      page,
    }) => {
      await clickCancelThisRequest(page, "button");
      await page.locator("form#cancel-request a").click();
      await expect(page).toHaveURL(Paths.MUST_SUBMIT_SUBJECT_ACCESS);
    });
  });
});
