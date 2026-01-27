import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  checkExternalLink,
  presentSubjectAccessRequest,
} from "../lib/step-functions";

test.describe("the 'Subject Access Request' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.SUBJECT_ACCESS_REQUEST);
  });

  test("is presented as expected", async ({ page }) => {
    await presentSubjectAccessRequest(page);
  });

  test("the 'Request a record for a living person born before or in 1939' link has the correct destination and is set to open in new tab", async ({
    page,
  }) => {
    await checkExternalLink(
      page,
      "Request a record for a living person born before or in 1939",
      "https://discovery.nationalarchives.gov.uk/mod-dsa-request-step1",
    );
  });

  test("the 'request a record for a living person born after or in 1940' link has the correct destination and is set to open in new tab", async ({
    page,
  }) => {
    await checkExternalLink(
      page,
      "request a record for a living person born after or in 1940",
      "https://www.gov.uk/get-copy-military-records-of-service/apply-for-your-own-records",
    );
  });
});
