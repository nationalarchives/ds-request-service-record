import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import { clickBackLink, continueFromJourneyStart } from "../lib/step-functions";

test.describe("the 'Request a military service record' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
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
