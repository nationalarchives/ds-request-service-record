import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromProvideAProofOfDeath,
} from "../lib/step-functions";
import { testfirstBirthYearForClosedRecords } from "../lib/test-first-birth-year-for-closed-records";

test.describe("The 'Provide a proof of death?' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.PROVIDE_A_PROOF_OF_DEATH);
  });

  test("has the correct value shown for last birth year for open records", async ({
    page,
  }) => {
    await testfirstBirthYearForClosedRecords(page);
  });

  test("clicking the 'Back' link takes the user to the 'What was their date of birth?' page", async ({
    page,
  }) => {
    await clickBackLink(page, Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH);
  });

  test.describe("when submitted", () => {
    test("without a selection, shows an error", async ({ page }) => {
      await continueFromProvideAProofOfDeath(page, false, null, null);
    });

    const selectionMappings = [
      {
        label: "Yes",
        nextUrl: Paths.UPLOAD_A_PROOF_OF_DEATH,
        heading: /Upload a proof of death/,
        description:
          'when "Yes" is selected, the user is directed to "Upload a proof of death" form and the "Back" link works as expected',
      },
      {
        label: "No",
        nextUrl:
          Paths.ARE_YOU_SURE_YOU_WANT_TO_PROCEED_WITHOUT_A_PROOF_OF_DEATH,
        heading: /Are you sure you want to proceed without a proof of death?/,
        description:
          'when "No" is selected, the user is directed to "Are you sure you want to proceed without a proof of death?" form and the "Back" link works as expected',
      },
    ];

    selectionMappings.forEach(({ label, nextUrl, heading, description }) => {
      test(description, async ({ page }) => {
        await continueFromProvideAProofOfDeath(page, label, nextUrl, heading);
        await clickBackLink(page, Paths.PROVIDE_A_PROOF_OF_DEATH);
      });
    });
  });
});
