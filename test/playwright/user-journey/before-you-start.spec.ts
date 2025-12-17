import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'Before you start' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.BEFORE_YOU_START);
  });

  test.describe("when first rendered", () => {
    test("has the correct heading", async ({ page }) => {
      await expect(page.locator("h1")).toHaveText(/Before you start/);
    });
  });

  test.describe("when interacted with", () => {
    test("clicking the 'Back' link takes the user to 'How we process requests'", async ({
      page,
    }) => {
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Paths.HOW_WE_PROCESS_REQUESTS);
    });

    test.describe("clicking the external links", () => {
      test("clicking the 'Copies of death certificates (opens in new tab)' link opens link in new tab", async ({
        page,
      }) => {
        const [newPage] = await Promise.all([
          page.waitForEvent("popup"), // waits for the new tab
          page
            .getByRole("link", {
              name: "Copies of death certificates (opens in new tab)",
            })
            .click(),
        ]);

        await newPage.waitForLoadState("domcontentloaded");

        expect(newPage.url()).toContain(
          "https://www.gov.uk/order-copy-birth-death-marriage-certificate",
        );
      });
      test("clicking the 'Commonwealth War Graves’ (CWG) war dead records (opens in new tab)' link opens link in new tab", async ({
        page,
      }) => {
        const [newPage] = await Promise.all([
          page.waitForEvent("popup"), // waits for the new tab
          page
            .getByRole("link", {
              name: "Commonwealth War Graves’ (CWG) war dead records (opens in new tab)",
            })
            .click(),
        ]);

        await newPage.waitForLoadState("domcontentloaded");

        expect(newPage.url()).toContain(
          "https://www.cwgc.org/find-records/find-war-dead/",
        );
      });
    });

    test.describe("clicking 'Start now'", () => {
      test("without selecting an option shows an error message", async ({
        page,
      }) => {
        await page.getByRole("button", { name: /Start now/i }).click();
        await expect(page.locator(".tna-error-summary__list")).toHaveText(
          /You must confirm you have the mandatory information before starting/,
        );
      });

      test("after checking the checkbox, takes user to 'You may want to check Ancestry' page", async ({
        page,
      }) => {
        await page
          .getByLabel(/I have all the mandatory information/)
          .check({ force: true });
        await page.getByRole("button", { name: /Start now/i }).click();
        await expect(page).toHaveURL(Paths.YOU_MAY_WANT_TO_CHECK_ANCESTRY);
      });

      test("having reached 'You may want to check Ancestry' page, clicking 'Back' brings the user back", async ({
        page,
      }) => {
        await page
          .getByLabel(/I have all the mandatory information/)
          .check({ force: true });
        await page.getByRole("button", { name: /Start now/i }).click();
        await expect(page).toHaveURL(Paths.YOU_MAY_WANT_TO_CHECK_ANCESTRY);
        await page.getByRole("link", { name: "Back" }).click();
        await expect(page).toHaveURL(Paths.BEFORE_YOU_START);
      });
    });

    test.describe("the 'Exit this form' link", () => {
      test("takes the user to the 'Are you sure you want to cancel?' page", async ({
        page,
      }) => {
        await page.getByRole("link", { name: "Exit this form" }).click();
        await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
      });
      test("having reached 'Are you sure you want to cancel?', clicking 'Back' brings the user back", async ({
        page,
      }) => {
        await page.getByRole("link", { name: "Exit this form" }).click();
        await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
        await page.getByRole("link", { name: "Back" }).click();
        await expect(page).toHaveURL(Paths.BEFORE_YOU_START);
      });
      test("having reached 'Are you sure you want to cancel?', clicking 'No' brings the user back", async ({
        page,
      }) => {
        await page.getByRole("link", { name: "Exit this form" }).click();
        await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
        await page.locator("#cancel-request a").click();
        await expect(page).toHaveURL(Paths.BEFORE_YOU_START);
      });
    });
  });
});
