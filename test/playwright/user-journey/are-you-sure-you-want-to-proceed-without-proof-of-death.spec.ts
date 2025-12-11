import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("The 'Are you sure you want to proceed without a proof of death?' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(
      Paths.ARE_YOU_SURE_YOU_WANT_TO_PROCEED_WITHOUT_A_PROOF_OF_DEATH,
    );
  });

  test.describe("when first rendered", () => {
    test("has the correct heading", async ({ page }) => {
      await expect(page.locator("h1")).toHaveText(
        /Are you sure you want to proceed without a proof of death?/,
      );
    });
  });

  test.describe("when submitted", () => {
    test("without a selection, shows an error", async ({ page }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-fieldset__error")).toHaveText(
        /You must confirm your selection to proceed/,
      );
    });

    const selectionMappings = [
      {
        label: "Yes, I would like to continue without a proof of death",
        url: Paths.SERVICE_PERSON_DETAILS,
        heading: /Tell us as much as you know about the service person/,
        description:
          'when "Yes" is selected, the user is directed to "Tell us as much as you know about the service person" form',
      },
      {
        label: "No, I would like to upload a proof of death",
        url: Paths.UPLOAD_A_PROOF_OF_DEATH,
        heading: /Upload a proof of death/,
        description:
          'when "No" is selected, the user is directed to "Upload a proof of death" form',
      },
    ];

    selectionMappings.forEach(({ label, url, heading, description }) => {
      test(description, async ({ page }) => {
        await page.getByLabel(label, { exact: true }).check();
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(url);
        await expect(page.locator("h1")).toHaveText(heading);
        await page.getByRole("link", { name: "Back" }).click();
        await expect(page).toHaveURL(
          Paths.ARE_YOU_SURE_YOU_WANT_TO_PROCEED_WITHOUT_A_PROOF_OF_DEATH,
        );
      });
    });
  });
});
