import { test, expect } from "@playwright/test";

test.describe("how do you want your order processed", () => {
  const basePath = "/request-a-military-service-record";

  enum Urls {
    START_PAGE = `${basePath}/start/`,
    YOUR_POSTAL_ADDRESS = `${basePath}/how-do-you-want-your-order-processed/`,
  }

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.START_PAGE);
    await page.goto(Urls.YOUR_POSTAL_ADDRESS);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /How do you want your order processed?/,
    );
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
          /You must select a processing option to continue/,
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
          /You must select a processing option to continue/,
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
  });
});
