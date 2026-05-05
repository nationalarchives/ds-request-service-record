import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromHaveYouPreviouslyMadeARequest,
} from "../lib/step-functions";

test.describe("have you previously made a request", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST);
  });

  test("clicking 'Back' from 'Have you previously made a request' brings the user back to the 'Service person details' page", async ({
    page,
  }) => {
    await clickBackLink(page, Paths.SERVICE_PERSON_DETAILS);
  });

  test.describe("when submitted", () => {
    test("without a selection, the user is shown an error message", async ({
      page,
    }) => {
      await continueFromHaveYouPreviouslyMadeARequest(page, {
        label: "",
        errorMessage:
          /Tell us if you have made a request for this record before/,
        populatedReferenceNumber: false,
      });
    });

    const selectionMappings = [
      {
        description:
          "with 'No' selected the user proceeds to the 'Choose your order type' page",
        label: "No",
        populatedReferenceNumber: false,
      },
      {
        description:
          "with MoD selected and no reference number provided, there is an error message",
        label: "Yes, to the Ministry of Defence",
        populatedReferenceNumber: false,
        errorMessage: /Enter the reference number for your previous request/,
      },
      {
        description:
          "with TNA selected and no reference number provided, there is an error message",
        label: "Yes, to The National Archives",
        populatedReferenceNumber: false,
        errorMessage: /Enter the reference number for your previous request/,
      },
      {
        description:
          "with TNA selected and an excessively long reference number provided, there is an error message",
        label: "Yes, to The National Archives",
        populatedReferenceNumber: "abcdefghijklmnopqrstuvwxyz".repeat(4),
        errorMessage: /Reference number must be 64 characters or less/,
      },
      {
        description:
          "with MoD selected and a reference number provided, the user proceeds to the 'Choose your order type' page",
        label: "Yes, to the Ministry of Defence",
        populatedReferenceNumber: "ABC 123",
      },
      {
        description:
          "with TNA selected and a reference number provided, the user proceeds to the 'Choose your order type' page",
        label: "Yes, to The National Archives",
        populatedReferenceNumber: "ABC 123",
      },
    ];

    selectionMappings.forEach(
      ({ description, label, errorMessage, populatedReferenceNumber }) => {
        test(description, async ({ page }) => {
          await continueFromHaveYouPreviouslyMadeARequest(page, {
            label,
            errorMessage,
            populatedReferenceNumber,
          });
        });
      },
    );
  });
});
