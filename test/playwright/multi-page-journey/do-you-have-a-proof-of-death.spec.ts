import { test, expect } from "@playwright/test";

test.describe("The 'Do you have a proof of death?' form", () => {
  const basePath = "/request-a-service-record";

  enum Urls {
    JOURNEY_START = `${basePath}/start/`,
    DO_YOU_HAVE_A_PROOF_OF_DEATH = `${basePath}/do-you-have-a-proof-of-death/`,
    UPLOAD_A_PROOF_OF_DEATH = `${basePath}/upload-a-proof-of-death/`,
  }

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.JOURNEY_START);
    await page.goto(Urls.DO_YOU_HAVE_A_PROOF_OF_DEATH);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/Provide a proof of death/);
  });

  test.describe("when submitted", () => {
    test("without a submission, shows an error", async ({ page }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-form__error-message")).toHaveText(
        /Choosing an option is required/,
      );
    });

    const selectionMappings = [
      {
        label: "Yes",
        url: Urls.UPLOAD_A_PROOF_OF_DEATH,
        heading: /Upload a proof of death/,
        description:
          'when "Yes" is selected, the user is directed to "Upload a proof of death" form',
      },
      {
        label: "No",
        url: Urls.UPLOAD_A_PROOF_OF_DEATH,
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
