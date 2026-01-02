import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromChooseYourOrderType,
} from "../lib/step-functions";

test.describe("choose your order type", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST);
    await page.goto(Paths.CHOOSE_YOUR_ORDER_TYPE);
  });

  test.describe("works as expected", () => {
    ["Choose standard", "Choose full record check"].forEach((buttonText) => {
      test(`selecting '${buttonText}' continues to 'Your order summary'`, async ({
        page,
      }) => {
        await continueFromChooseYourOrderType(page, buttonText);
      });

      test(`clicking 'Back' from 'Your order summary' after selecting '${buttonText}' returns to 'Choose your order type'`, async ({
        page,
      }) => {
        await continueFromChooseYourOrderType(page, buttonText);
        await clickBackLink(page, Paths.CHOOSE_YOUR_ORDER_TYPE);
      });
    });
  });
});
