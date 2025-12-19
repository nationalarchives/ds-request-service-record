import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromHowWeProcessRequests,
} from "../lib/step-functions";

test.describe("the 'How we process requests' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.HOW_WE_PROCESS_REQUESTS);
  });

  test("works as expected", async ({ page }) => {
    await continueFromHowWeProcessRequests(page);
  });

  test("clicking the 'Back' link on the next page brings the user back", async ({
    page,
  }) => {
    await continueFromHowWeProcessRequests(page);
    await clickBackLink(page, Paths.HOW_WE_PROCESS_REQUESTS);
  });
});
