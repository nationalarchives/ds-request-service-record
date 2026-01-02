import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromAreYouSureYouWantToProceedWithoutAProofOfDeath,
} from "../lib/step-functions";

test.describe("The 'Are you sure you want to proceed without a proof of death?' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(
      Paths.ARE_YOU_SURE_YOU_WANT_TO_PROCEED_WITHOUT_A_PROOF_OF_DEATH,
    );
  });

  test("clicking the 'Back' link takes the user to the 'Provide a proof of death' page", async ({
    page,
  }) => {
    await clickBackLink(page, Paths.PROVIDE_A_PROOF_OF_DEATH);
  });

  test.describe("when submitted", () => {
    test("without a selection, shows an error", async ({ page }) => {
      await continueFromAreYouSureYouWantToProceedWithoutAProofOfDeath(
        page,
        false,
        null,
        null,
      );
    });

    const selectionMappings = [
      {
        label: "Yes, I would like to continue without a proof of death",
        nextUrl: Paths.SERVICE_PERSON_DETAILS,
        heading: /Tell us as much as you know about the service person/,
        description:
          'when "Yes" is selected, the user is directed to "Tell us as much as you know about the service person" form',
      },
      {
        label: "No, I would like to upload a proof of death",
        nextUrl: Paths.UPLOAD_A_PROOF_OF_DEATH,
        heading: /Upload a proof of death/,
        description:
          'when "No" is selected, the user is directed to "Upload a proof of death" form',
      },
    ];

    selectionMappings.forEach(({ label, nextUrl, heading, description }) => {
      test(description, async ({ page }) => {
        await continueFromAreYouSureYouWantToProceedWithoutAProofOfDeath(
          page,
          label,
          nextUrl,
          heading,
        );
        await clickBackLink(
          page,
          Paths.ARE_YOU_SURE_YOU_WANT_TO_PROCEED_WITHOUT_A_PROOF_OF_DEATH,
        );
      });
    });
  });
});
