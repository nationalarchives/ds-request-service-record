import { test, expect } from "@playwright/test";

test.describe("'Have you checked the catalogue?' form", () => {
  const basePath = "/request-a-service-record";

  enum Urls {
    JOURNEY_START = `${basePath}/start/`,
    HAVE_YOU_CHECKED_THE_CATALOGUE = `${basePath}/have-you-checked-the-catalogue/`,
    IS_SERVICE_PERSON_ALIVE = `${basePath}/is-service-person-alive/`,
    SEARCH_THE_CATALOGUE = `${basePath}/search-the-catalogue/`,
  }

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.JOURNEY_START);
    await page.goto(Urls.HAVE_YOU_CHECKED_THE_CATALOGUE);
  });

  test("Has the right heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /Have you checked if this record is available in our catalogue\?/,
    );
  });

  test("clicking 'Continue' without having made a selection keeps the user on the page and shows a validation error", async ({
    page,
  }) => {
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page).toHaveURL(Urls.HAVE_YOU_CHECKED_THE_CATALOGUE);
    await expect(page.locator(".tna-form__error-message")).toHaveText(
      /Choosing an option is required/,
    );
  });

  const selectionMappings = [
    {
      label: "Yes",
      url: Urls.IS_SERVICE_PERSON_ALIVE,
      heading: /Is this person still alive\?/,
      description:
        "Presents the 'Is this person still alive?' page when 'Yes' is selected",
    },
    {
      label: "No",
      url: Urls.SEARCH_THE_CATALOGUE,
      heading: "Search our catalogue",
      description:
        "Presents the 'Search our catalogue' page when 'No' is selected",
    },
  ];

  test.describe("Selecting an option and continuing", () => {
    selectionMappings.forEach(({ label, url, heading, description }) => {
      test(description, async ({ page }) => {
        await page.getByLabel(label, { exact: true }).check();
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(url);
        await expect(page.locator("h1")).toHaveText(heading);
      });
    });
  });

  test.describe("Having submitted a selection, clicking the 'Back' link ", () => {
    selectionMappings.forEach(({ label, url, heading }) => {
      test(`when ${label} is submitted, ${label} is selected when the user returns`, async ({ page }) => {
        await page.getByLabel(label, { exact: true }).check();
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(url);
        await expect(page.locator("h1")).toHaveText(heading);
        await page.getByRole("link", { name: "Back" }).click();
        await expect(page).toHaveURL(Urls.HAVE_YOU_CHECKED_THE_CATALOGUE);
        await expect(page.getByLabel(label, { exact: true })).toBeChecked();
      });
    });
  });
});
