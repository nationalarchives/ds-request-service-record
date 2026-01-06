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
      orderTypePrice: "£47.16",
      deliveryFee: "£7.95",
      description: "Standard",
      personMakingRequest: {
        firstName: "Francis",
        lastName: "Palgrave",
      },
    },
    {
      buttonText: "full",
      orderTypePrice: "£48.87",
      description: "Full record check",
      personMakingRequest: {
        firstName: "Francis",
        lastName: "Palgrave",
      },
    },
  ];

  for (const {
    buttonText,
    orderTypePrice,
    deliveryFee,
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
      await expect(page.locator("[data-price]")).toHaveText(
        new RegExp(orderTypePrice),
      );
      if (deliveryFee) {
        await expect(page.locator("[data-delivery-price]")).toHaveText(
          new RegExp(deliveryFee),
        );
      }
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
      orderTypePrice: "£42.25",
      description: "Standard",
      personMakingRequest: {
        firstName: "Francis",
        lastName: "Palgrave",
        emailAddress: "test@example.com",
      },
    },
    {
      buttonText: "Choose full record check",
      orderTypePrice: "£48.87",
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
    orderTypePrice,
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
      await expect(page.locator("[data-price]")).toHaveText(
        new RegExp(orderTypePrice),
      );
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
