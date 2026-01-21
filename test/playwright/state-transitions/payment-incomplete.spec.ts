import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import { continueFromPaymentIncomplete } from "../lib/step-functions";

test.describe("the 'Payment incomplete' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.PAYMENT_INCOMPLETE);
  });

  test.describe("works as expected", () => {
    test("when continuing to 'Your order summary'", async ({ page }) => {
      await continueFromPaymentIncomplete(page);
    });
  });
});
