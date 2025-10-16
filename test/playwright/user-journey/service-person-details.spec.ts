import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'About the service person form?' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Paths.SERVICE_PERSON_DETAILS);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/About the service person/);
  });

  test.describe("when submitted", () => {
    test.describe("with invalid input", () => {
      test("without any input, the validation summary is shown", async ({
        page,
      }) => {
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page.locator(".tna-error-summary")).toHaveText(
          /There is a problem/,
        );
      });
      test("and errors are shown against only the required fields", async ({
        page,
      }) => {
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page.locator(".tna-form-item__error")).toHaveCount(2);
        await expect(page.locator(".tna-form-item__error").first()).toHaveText(
          /The service person's first name is required/,
        );
        await expect(page.locator(".tna-form-item__error").nth(1)).toHaveText(
          /The service person's last name is required/,
        );
      });
    });
    test.describe("with valid input", () => {
      test("with only the required fields filled in, the user is taken to the next page", async ({
        page,
      }) => {
        await page.getByLabel("First name").fill("Thomas");
        await page.getByLabel("Last name", { exact: true }).fill("Duffus");
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(Paths.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST);
      });
      test("with all fields filled in, the user is taken to the next page", async ({
        page,
      }) => {
        await page.getByLabel("First name").fill("Thomas");
        await page.getByLabel("Middle names").fill("Duffus");
        await page.getByLabel("Last name", { exact: true }).fill("Hardy");
        await page.getByLabel("Service number").fill("123456");
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(Paths.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST);
      });
    });
  });
});
