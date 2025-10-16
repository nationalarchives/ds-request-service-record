import { test, expect } from "@playwright/test";

test.describe("have you previously made a request", () => {
  const basePath = "/request-a-military-service-record";
  enum Urls {
    START_PAGE = `${basePath}/start/`,
    HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST = `${basePath}/have-you-previously-made-a-request/`,
    YOUR_DETAILS = `${basePath}/your-details/`,
    SERVICE_PERSON_DETAILS = `${basePath}/service-person-details/`,
  }

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.START_PAGE);
    await page.goto(Urls.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /Have you previously made a request/,
    );
  });

  test.describe("when submitted", () => {
    test("the user is taken to the 'Your details' page", async ({ page }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(Urls.YOUR_DETAILS);
      await expect(page.locator("h1")).toHaveText(/Your details/);
    });

    test("clicking 'Back' from 'Have you previously made a request?' brings the user back to the 'Service person details' page", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Urls.SERVICE_PERSON_DETAILS);
    });
  });
});
