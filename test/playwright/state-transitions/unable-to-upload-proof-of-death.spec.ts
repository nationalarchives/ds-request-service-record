import { expect, test } from "@playwright/test";
import { Paths } from "../lib/constants";
import { presentUnableToUploadProofOfDeath } from "../lib/step-functions";

test.describe("the 'Sorry, we were unable to upload your file' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.UNABLE_TO_PROVIDE_PROOF_OF_DEATH);
  });

  test("is presented as expected", async ({ page }) => {
    await presentUnableToUploadProofOfDeath(page);
  });

  test("works as expected", async ({ page }) => {
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page).toHaveURL(Paths.SERVICE_PERSON_DETAILS);
    await expect(page.locator("h1")).toHaveText(
      /Tell us as much as you know about the service person/,
    );
  });
});
