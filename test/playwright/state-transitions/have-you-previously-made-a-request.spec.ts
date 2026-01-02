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
      await continueFromHaveYouPreviouslyMadeARequest(
        page,
        "",
        /Tell us if you have made a request for this record before/,
        false,
      );
    });

    const selectionMappings = [
      {
        description:
          "with 'No' selected the user proceeds to the 'Choose your order type' page",
        label: "No",
        populateReferenceNumber: false,
      },
      {
        description:
          "with MoD selected and no reference number provided, there is an error message",
        label: "Yes, to the Ministry of Defence",
        populateReferenceNumber: false,
        errorMessage: /Enter the reference number for your previous request/,
      },
      {
        description:
          "with TNA selected and no reference number provided, there is an error message",
        label: "Yes, to The National Archives",
        populateReferenceNumber: false,
        errorMessage: /Enter the reference number for your previous request/,
      },
      {
        description:
          "with MoD selected and a reference number provided, the user proceeds to the 'Choose your order type' page",
        label: "Yes, to the Ministry of Defence",
        populateReferenceNumber: true,
      },
      {
        description:
          "with TNA selected and a reference number provided, the user proceeds to the 'Choose your order type' page",
        label: "Yes, to The National Archives",
        populateReferenceNumber: true,
      },
    ];

    selectionMappings.forEach(
      ({ description, label, errorMessage, populateReferenceNumber }) => {
        test(description, async ({ page }) => {
          await continueFromHaveYouPreviouslyMadeARequest(
            page,
            label,
            errorMessage,
            populateReferenceNumber,
          );
        });
      },
    );
  });
});
