import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromChooseYourOrderType,
  continueFromYourContactDetails,
  continueFromYourPostalAddress,
} from "../lib/step-functions";

test.describe("Routes to 'Your order summary'", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.CHOOSE_YOUR_ORDER_TYPE);
  });

  const providedByPostTests = [
    {
      buttonText: "standard",
      price: "£51.66",
      description: "Standard",
      personMakingRequest: {
        firstName: "Francis",
        lastName: "Palgrave",
      },
    },
    {
      buttonText: "full",
      price: "£48.87",
      description: "Full record check",
      personMakingRequest: {
        firstName: "Francis",
        lastName: "Palgrave",
      },
    },
  ];

  for (const {
    buttonText,
    price,
    description,
    personMakingRequest,
  } of providedByPostTests) {
    test(`we're presenting the correct information for a ${description.toLowerCase()} order provided by post`, async ({
      page,
    }) => {
      await continueFromChooseYourOrderType(page, buttonText);
      await continueFromYourContactDetails(page, personMakingRequest);
      await continueFromYourPostalAddress(page);
      await expect(page.locator("#processing-option")).toHaveText(
        new RegExp(description),
      );
      await expect(page.locator("#price")).toHaveText(new RegExp(price));
      await expect(page.locator("#price")).toHaveText(
        /plus £1.04 per page copying fee/,
      );
      await clickBackLink(page, Paths.WHAT_IS_YOUR_ADDRESS);
    });

    test(`the postal address user is able to change their order selection from the order summary page for ${description.toLowerCase()}`, async ({
      page,
    }) => {
      await continueFromChooseYourOrderType(page, buttonText);
      await continueFromYourContactDetails(page, personMakingRequest);
      await continueFromYourPostalAddress(page);
      await page.getByRole("link", { name: "Change order" }).click();
      await expect(page).toHaveURL(Paths.CHOOSE_YOUR_ORDER_TYPE);
    });
  }

  const providedByEmailTests = [
    {
      buttonText: "Choose standard",
      price: "£42.25",
      description: "Standard",
      personMakingRequest: {
        firstName: "Francis",
        lastName: "Palgrave",
        emailAddress: "test@example.com",
      },
    },
    {
      buttonText: "Choose full record check",
      price: "£48.87",
      description: "Full record check",
      personMakingRequest: {
        firstName: "Francis",
        lastName: "Palgrave",
        emailAddress: "test@example.com",
      },
    },
  ];

  for (const {
    buttonText,
    price,
    description,
    personMakingRequest,
  } of providedByEmailTests) {
    test(`we're presenting the correct information for a ${description.toLowerCase()} order provided by email`, async ({
      page,
    }) => {
      await continueFromChooseYourOrderType(page, buttonText);
      await continueFromYourContactDetails(page, personMakingRequest);
      await expect(page.locator("#processing-option")).toHaveText(
        new RegExp(description),
      );
      await expect(page.locator("#price")).toHaveText(new RegExp(price));
      await clickBackLink(page, Paths.YOUR_CONTACT_DETAILS);
    });

    test(`the email user is able to change their order selection from the order summary page for ${description.toLowerCase()}`, async ({
      page,
    }) => {
      await continueFromChooseYourOrderType(page, buttonText);
      await continueFromYourContactDetails(page, personMakingRequest);
      await page.getByRole("link", { name: "Change order" }).click();
      await expect(page).toHaveURL(Paths.CHOOSE_YOUR_ORDER_TYPE);
    });
  }
});
