import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import { continueFromAreYouSureYouWantToCancel } from "../lib/step-functions";

test.describe("the 'Are you sure you want to cancel?' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
  });

  test.describe("works as expected", () => {
    test("when continuing to cancel", async ({ page }) => {
      await continueFromAreYouSureYouWantToCancel(page, true);
    });
  });
});
