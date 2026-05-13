import { expect, test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  continueFromChooseYourOrderType,
  continueFromPaymentIncomplete,
  continueFromYourContactDetails,
} from "../lib/step-functions";

test.describe("the 'Problem processing payment' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.PAYMENT_INCOMPLETE);
  });

  test.describe("works as expected when attempting to continue to 'Your order summary'", () => {
    test.describe("'Your order summary' can be reached", () => {
      test("when the steps necessary to populate relevant session values have been followed", async ({
        page,
      }) => {
        await page.goto(Paths.CHOOSE_YOUR_ORDER_TYPE);
        await continueFromChooseYourOrderType(page, "Choose standard");
        await continueFromYourContactDetails(page, {
          firstName: "Francis",
          lastName: "Palgrave",
          emailAddress: "test@example.com",
        });
        await page.goto(Paths.PAYMENT_INCOMPLETE);

        await continueFromPaymentIncomplete(page);
      });
    });

    test.describe("'Your order summary' cannot be reached", () => {
      test("when the steps necessary to populate relevant session values have NOT been followed", async ({
        page,
      }) => {
        await expect(page).toHaveURL(Paths.PAYMENT_INCOMPLETE);
        await expect(page.locator("h1")).toHaveText(
          /Sorry, there was a problem processing your payment/,
        );
        await page
          .getByRole("button", { name: "Go back to try the payment again" })
          .click();
        await expect(page).toHaveURL(Paths.JOURNEY_START);
      });
    });
  });
});
