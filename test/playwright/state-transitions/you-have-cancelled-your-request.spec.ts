import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import { continueFromYouHaveCancelledYourRequest } from "../lib/step-functions";

test.describe("the 'You have cancelled your request' page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.YOU_HAVE_CANCELLED_YOUR_REQUEST);
  });

  test.describe("when interacted with", () => {
    test("clicking 'Start a new request' takes the user to the start page", async ({
      page,
    }) => {
      await continueFromYouHaveCancelledYourRequest(page);
    });
  });
});
