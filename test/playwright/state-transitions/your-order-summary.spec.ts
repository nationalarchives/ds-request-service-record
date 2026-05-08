import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromChooseYourOrderType,
  continueFromYourContactDetails,
  continueFromYourPostalAddress,
  continueToChooseYourOrderTypeFromJourneyStart,
} from "../lib/step-functions";

test.describe("Routes to 'Your order summary'", () => {
  test.beforeEach(async ({ page }) => {
    test.setTimeout(120_000); // Increase timeout to 2 minutes for this test because it is end-to-end
    await continueToChooseYourOrderTypeFromJourneyStart(page, {
      isAlive: "No",
      serviceBranch: "British Army",
      wasOfficer: "No",
    });
  });

  const providedByPostTests = [
    {
      buttonText: "standard",
      totalPrice: "55.11",
      orderTypePrice: "47.16",
      deliveryFee: "7.95",
      description: "Standard",
      personMakingRequest: {
        firstName: "Francis",
        lastName: "Palgrave",
      },
    },
    {
      buttonText: "full",
      totalPrice: "48.87",
      description: "Full record check",
      personMakingRequest: {
        firstName: "Francis",
        lastName: "Palgrave",
      },
    },
  ];

  for (const {
    buttonText,
    totalPrice,
    deliveryFee,
    orderTypePrice,
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
        new RegExp(totalPrice),
      );
      if (orderTypePrice) {
        await expect(page.locator("[data-order-type-price]")).toHaveText(
          new RegExp(orderTypePrice),
        );
      }
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

test.describe("'Change order' availability rules on 'Your order summary'", () => {
  // These are just a sample of combinations - the full range of combinations is
  // covered by unit tests.
  const changeOrderAvailabilityScenarios = [
    {
      description: "when the service person was not an officer",
      serviceBranch: "British Army",
      wasOfficer: "No",
      nextUrlAfterOfficerSelection: Paths.WE_MAY_HOLD_THIS_RECORD,
      expectedTemplateIdentifier: "we-may-hold-this-record--generic",
      isChangeOrderAvailable: true,
    },
    {
      description:
        "when the service person was an officer in the Royal Air Force",
      serviceBranch: "Royal Air Force",
      wasOfficer: "Yes",
      nextUrlAfterOfficerSelection:
        Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__RAF,
      expectedTemplateIdentifier: "unlikely-to-hold--raf-officer-records",
      isChangeOrderAvailable: true,
    },
    {
      description: "when the service person was an officer in a non-RAF branch",
      serviceBranch: "British Army",
      wasOfficer: "Yes",
      nextUrlAfterOfficerSelection:
        Paths.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY,
      expectedTemplateIdentifier: "unlikely-to-hold--army-officer-records",
      isChangeOrderAvailable: false,
    },
    {
      description: "when officer status is unknown",
      serviceBranch: "Royal Air Force",
      wasOfficer: "I do not know",
      nextUrlAfterOfficerSelection: Paths.WE_MAY_HOLD_THIS_RECORD,
      expectedTemplateIdentifier: "we-may-hold-this-record--generic",
      isChangeOrderAvailable: false,
    },
  ];

  for (const scenario of changeOrderAvailabilityScenarios) {
    test(`the 'Change order' link is ${scenario.isChangeOrderAvailable ? "" : "not "}shown ${scenario.description}`, async ({
      page,
    }) => {
      await continueToChooseYourOrderTypeFromJourneyStart(page, scenario);
      await continueFromChooseYourOrderType(page, "Choose standard");
      await continueFromYourContactDetails(page, {
        firstName: "Francis",
        lastName: "Palgrave",
        emailAddress: "test@example.com",
      });

      const changeOrderLink = page.getByRole("link", { name: "Change order" });

      if (scenario.isChangeOrderAvailable) {
        await expect(changeOrderLink).toBeVisible();
        await changeOrderLink.click();
        await expect(page).toHaveURL(Paths.CHOOSE_YOUR_ORDER_TYPE);
      } else {
        await expect(changeOrderLink).toHaveCount(0);
      }
    });
  }
});
