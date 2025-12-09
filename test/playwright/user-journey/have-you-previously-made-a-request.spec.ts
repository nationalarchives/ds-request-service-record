import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("have you previously made a request", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /Have you previously made a request/,
    );
  });

  test.describe("when submitted", () => {
    test("without a selection, the user is shown an error message", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-fieldset__error")).toHaveText(
        /Please select an option/,
      );
    });

    const selectionMappings = [
      {
        description:
          "with MoD selected and no reference number provided, there is an error message",
        label: "Yes, to the Ministry of Defence",
        populateReferenceNumber: false,
        errorMessage: /Enter the reference number for your previous request/,
      },
      {
        description:
          "with TNA selected and no reference number provided, there is an error message",
        label: "Yes, to The National Archives",
        populateReferenceNumber: false,
        errorMessage: /Enter the reference number for your previous request/,
      },
      {
        description:
          "with MoD selected and a reference number provided, the user proceeds to the 'Choose your order type' page",
        label: "Yes, to the Ministry of Defence",
        populateReferenceNumber: true,
        expectedHeading: /Choose your order type/,
      },
      {
        description:
          "with TNA selected and a reference number provided, the user proceeds to the 'Choose your order type' page",
        label: "Yes, to The National Archives",
        populateReferenceNumber: true,
        expectedHeading: /Choose your order type/,
      },
    ];

    selectionMappings.forEach(
      ({
        description,
        label,
        errorMessage,
        populateReferenceNumber,
        expectedHeading,
      }) => {
        test(description, async ({ page }) => {
          await page.getByLabel(label, { exact: true }).check();

          if (populateReferenceNumber) {
            await page.getByLabel("Reference number").fill("ABC123");
            await page.getByRole("button", { name: /Continue/i }).click();
            await expect(page).toHaveURL(Paths.CHOOSE_YOUR_ORDER_TYPE);
            await expect(page.locator("h1")).toHaveText(
              /Choose your order type/,
            );
          } else {
            await page.getByRole("button", { name: /Continue/i }).click();
            await expect(page.locator(".tna-error-summary")).toHaveText(
              errorMessage,
            );
          }
        });
      },
    );
  });

  test("with 'No' selected, the user is taken to the 'Choose your order type' page", async ({
    page,
  }) => {
    await page.getByLabel("No", { exact: true }).check();
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page).toHaveURL(Paths.CHOOSE_YOUR_ORDER_TYPE);
    await expect(page.locator("h1")).toHaveText(/Choose your order type/);
  });

  test("clicking 'Back' from 'Have you previously made a request' brings the user back to the 'Service person details' page", async ({
    page,
  }) => {
    await page.getByRole("link", { name: "Back" }).click();
    await expect(page).toHaveURL(Paths.SERVICE_PERSON_DETAILS);
  });
});
