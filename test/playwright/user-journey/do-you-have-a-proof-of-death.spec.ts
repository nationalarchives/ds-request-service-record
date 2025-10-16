import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("The 'Do you have a proof of death?' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.DO_YOU_HAVE_A_PROOF_OF_DEATH);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/Provide a proof of death/);
  });

  test.describe("when submitted", () => {
    test("without a submission, shows an error", async ({ page }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-fieldset__error")).toHaveText(
        /Choosing an option is required/,
      );
    });

    const selectionMappings = [
      {
        label: "Yes",
        url: Paths.UPLOAD_A_PROOF_OF_DEATH,
        heading: /Upload a proof of death/,
        description:
          'when "Yes" is selected, the user is directed to "Upload a proof of death" form',
      },
      {
        label: "No",
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
      });
    });
  });
});
