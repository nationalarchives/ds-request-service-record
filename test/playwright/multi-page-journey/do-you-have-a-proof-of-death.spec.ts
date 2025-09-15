import { test, expect } from "@playwright/test";

test.describe("The 'Do you have a proof of death?' form", () => {
  const basePath = "/request-a-service-record";

  enum Urls {
    JOURNEY_START = `${basePath}/start/`,
    DO_YOU_HAVE_A_PROOF_OF_DEATH = `${basePath}/do-you-have-a-proof-of-death`,
  }

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.JOURNEY_START);
    await page.goto(Urls.DO_YOU_HAVE_A_PROOF_OF_DEATH);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/Provide a proof of death/);
  });
});
