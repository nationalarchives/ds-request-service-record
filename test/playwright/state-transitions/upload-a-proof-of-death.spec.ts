import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromUploadAProofOfDeath,
} from "../lib/step-functions";

test.describe("The 'Upload a proof of death' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.PROVIDE_A_PROOF_OF_DEATH);
    await page.goto(Paths.UPLOAD_A_PROOF_OF_DEATH);
  });

  test("the form should have the enctype='multipart/form-data'", async ({
    page,
  }) => {
    // We need this for file uploads to work. Adding a specific test because it's easy to miss.
    await expect(page.locator("form")).toHaveAttribute(
      "enctype",
      "multipart/form-data",
    );
  });

  test.describe("when interacted with", () => {
    test("clicking the 'Back' link takes the user to the 'Provide a proof of death' page", async ({
      page,
    }) => {
      await clickBackLink(page, Paths.PROVIDE_A_PROOF_OF_DEATH);
    });
  });

  test.describe("when submitted", () => {
    const bufferSizeBelowLimit = 1024 * 1024 * 4; // 4MB
    const bufferSizeAboveLimit = 1024 * 1024 * 6; // 6MB

    test("when the form is submitted without a file selected, the user is presented with the next page", async ({
      page,
    }) => {
      await continueFromUploadAProofOfDeath(page, "", 0, true, null);
    });

    test("with an uploaded file with the incorrect extension, shows an error", async ({
      page,
    }) => {
      await continueFromUploadAProofOfDeath(
        page,
        ".docx",
        bufferSizeBelowLimit,
        false,
        /The selected file must be a JPG, JPEG, GIF or PNG/,
      );
    });

    ["jpg", "jpeg", "gif", "png"].forEach((extension) => {
      test(`with a valid extension (of .${extension}) which is above the size limit, shows an error`, async ({
        page,
      }) => {
        await continueFromUploadAProofOfDeath(
          page,
          `.${extension}`,
          bufferSizeAboveLimit,
          false,
          /The selected file must be smaller than 5MB/,
        );
      });

      test(`with a file that has a valid extention (of .${extension}) and is below the size limit, presents next page and the 'Back' link works as expected`, async ({
        page,
      }) => {
        await continueFromUploadAProofOfDeath(
          page,
          `.${extension}`,
          bufferSizeBelowLimit,
          true,
          null,
        );

        // Now test that the 'Back' link works as expected
        await clickBackLink(page, Paths.UPLOAD_A_PROOF_OF_DEATH);
      });
    });
  });
});
