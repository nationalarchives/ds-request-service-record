import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromJourneyStart,
  checkInternalLink,
  checkExternalLink,
} from "../lib/step-functions";

test.describe("the 'Request a military service record' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
  });

  test("has the correct links", async ({ page }) => {
    await checkInternalLink(
      page,
      "British Army soldiers of the First World War research guide",
      "https://www.nationalarchives.gov.uk/help-with-your-research/research-guides/british-army-soldiers-of-the-first-world-war/",
    );
    await checkExternalLink(
      page,
      "prices we charge (opens in new tab)",
      "https://www.nationalarchives.gov.uk/legal/our-fees/",
    );
  });

  test("works as expected", async ({ page }) => {
    await continueFromJourneyStart(page);
  });

  test("clicking the 'Back' link on the next page brings the user back", async ({
    page,
  }) => {
    await continueFromJourneyStart(page);
    await clickBackLink(page, Paths.JOURNEY_START);
  });
});
