import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("The 'Have you checked the catalogue?' form", () => {
  const selectionMappings = [
    {
      label: "Yes",
      url: Paths.IS_SERVICE_PERSON_ALIVE,
      heading: /Is the service person still alive\?/,
      description:
        "when 'Yes' is selected, presents the 'Is the service person still alive?' page ",
    },
    {
      label: "No",
      url: Paths.SEARCH_THE_CATALOGUE,
      heading: "Search our catalogue",
      description:
        "when 'No' is selected, presents the 'Search our catalogue' page ",
    },
  ];

  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.HAVE_YOU_CHECKED_THE_CATALOGUE);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /Have you checked if this record is available in our catalogue\?/,
    );
  });

  test.describe("when submitted", () => {
    const selectionMappings = [
      {
        label: "Yes",
        url: Paths.IS_SERVICE_PERSON_ALIVE,
        heading: /Is the service person still alive\?/,
        description:
          "when 'Yes' is selected, presents the 'Is the service person still alive?' page",
      },
      {
        label: "No",
        url: Paths.SEARCH_THE_CATALOGUE,
        heading: "Search our catalogue",
        description:
          "when 'No' is selected, presents the 'Search our catalogue' page",
      },
    ];
    test("without a selection, keeps the user on the page and shows a validation error", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page).toHaveURL(Paths.HAVE_YOU_CHECKED_THE_CATALOGUE);
      await expect(page.locator(".tna-fieldset__error")).toHaveText(
        /Choosing an option is required/,
      );
    });

    selectionMappings.forEach(({ label, url, heading, description }) => {
      test(description, async ({ page }) => {
        await page.getByLabel(label, { exact: true }).check();
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(url);
        await expect(page.locator("h1")).toHaveText(heading);
      });
    });
  });

  test.describe("clicking the 'Back' link after a submission", () => {
    selectionMappings.forEach(({ label, url, heading }) => {
      test(`when '${label}' was submitted, '${label}' is selected when the user returns`, async ({
        page,
      }) => {
        await page.getByLabel(label, { exact: true }).check();
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(url);
        await expect(page.locator("h1")).toHaveText(heading);
        await page.getByRole("link", { name: "Back" }).click();
        await expect(page).toHaveURL(Paths.HAVE_YOU_CHECKED_THE_CATALOGUE);
        await expect(page.getByLabel(label, { exact: true })).toBeChecked();
      });
    });
  });
});
