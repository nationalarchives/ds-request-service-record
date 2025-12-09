import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("choose your order type", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.CHOOSE_YOUR_ORDER_TYPE);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/Choose your order type/);
  });

  test.describe("when submitted", () => {
    test.describe("the 'standard' order form option", () => {
      test("without any fields selected, shows the correct error message", async ({
        page,
      }) => {
        await page
          .getByRole("button", { name: /Continue with a standard order/i })
          .click();
        await expect(page.locator(".tna-fieldset__error")).toHaveCount(1);
        await expect(page.locator(".tna-fieldset__error").first()).toHaveText(
          /Select how you would like your order processed/,
        );
      });
      ["Digital standard", "Printed standard"].forEach((option) => {
        test(`with "${option}" selected, there is no error`, async ({
          page,
        }) => {
          await page.getByLabel(option).check();
          await page
            .getByRole("button", { name: /Continue with a standard order/i })
            .click();
          await expect(page.locator(".tna-fieldset__error")).toHaveCount(0);
        });
      });
    });
    test.describe("the 'full' order form option", () => {
      test("without any fields selected, shows the correct error message", async ({
        page,
      }) => {
        await page
          .getByRole("button", {
            name: /Continue with a full record check order/i,
          })
          .click();
        await expect(page.locator(".tna-fieldset__error")).toHaveCount(1);
        await expect(page.locator(".tna-fieldset__error").first()).toHaveText(
          /Select how you would like your order processed/,
        );
      });
      ["Digital full record check", "Printed full record check"].forEach(
        (option) => {
          test(`with "${option}" selected, there is no error`, async ({
            page,
          }) => {
            await page.getByLabel(option).check();
            await page
              .getByRole("button", {
                name: /Continue with a full record check order/i,
              })
              .click();
            await expect(page.locator(".tna-fieldset__error")).toHaveCount(0);
          });
        },
      );
    });

    test("clicking 'Back' from 'Choose your order type' brings the user back to the 'Have you previously made a request' page", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Paths.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST);
    });
  });
});
