import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'Is the person still alive?' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Paths.IS_SERVICE_PERSON_ALIVE);
  });

  test.describe("when first rendered", () => {
    test("has the correct heading", async ({ page }) => {
      await expect(page.locator("h1")).toHaveText(
        /Is the service person alive\?/,
      );
    });
  });

  test.describe("when interacted with", () => {
    test("clicking the 'Back' link takes the user to the 'Have you checked the catalogue? page'", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Paths.YOU_MAY_WANT_TO_CHECK_ANCESTRY);
    });

    test("clicking 'Continue' without a selection, shows an error", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-fieldset__error")).toHaveText(
        /Tell us if the service person is alive/,
      );
    });

    const selectionMappings = [
      {
        label: "Yes",
        url: Paths.MUST_SUBMIT_SUBJECT_ACCESS,
        heading: /Submit a data access request/,
        description:
          "when 'Yes' is selected, presents the 'Submit a data access request' page ",
      },
      {
        label: "No",
        url: Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN,
        heading: /Which military branch did the person serve in\?/,
        description:
          "when 'No' is selected, presents the 'Which military branch did the person serve in?' form",
      },
      {
        label: "I do not know",
        url: Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN,
        heading: /Which military branch did the person serve in\?/,
        description:
          "when 'I do not know' is selected, presents the 'Which military branch did the person serve in?' form",
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

    test.describe("clicking the 'Back' link after a submission", () => {
      selectionMappings.forEach(({ label, url, heading }) => {
        test(`when '${label}' was submitted, clicking 'Back' brings the user back to 'Is the service person alive?' with '${label}' selected`, async ({
          page,
        }) => {
          await page.getByLabel(label, { exact: true }).check();
          await page.getByRole("button", { name: /Continue/i }).click();
          await expect(page).toHaveURL(url);
          await expect(page.locator("h1")).toHaveText(heading);
          await page.getByRole("link", { name: "Back" }).click();
          await expect(page).toHaveURL(Paths.IS_SERVICE_PERSON_ALIVE);
          await expect(page.getByLabel(label, { exact: true })).toBeChecked();
        });
      });
    });
  });
});
