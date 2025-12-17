import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'Submit a data access request' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.MUST_SUBMIT_SUBJECT_ACCESS);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/Submit a data access request/);
  });

  // test("clicking the 'Back' link takes the user to the 'Is the service person alive? page'", async ({
  //   page,
  // }) => {
  //   await page.getByRole("link", { name: "Back" }).click();
  //   await expect(page).toHaveURL(Paths.IS_SERVICE_PERSON_ALIVE);
  // });

  test.describe("clicking the 'Submit a data access request' button", () => {
    test("opens link in new tab", async ({ page }) => {
      // Trigger that opens a new tab (e.g. <a target="_blank">)
      const [newPage] = await Promise.all([
        page.waitForEvent("popup"), // waits for the new tab
        page
          .getByRole("link", { name: "Submit a data access request" })
          .click(),
      ]);

      await newPage.waitForLoadState("domcontentloaded");

      // Assertions on the new tab
      expect(newPage.url()).toContain(
        "https://discovery.nationalarchives.gov.uk/mod-dsa-request-step1",
      );
    });
  });

  test.describe("'Exit this form' and 'Back' links", () => {
    test("clicking the 'Exit this form' button takes the user to 'Are you sure you want to cancel?'", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Exit this form/i }).click();
      await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
    });

    // test("clicking the 'Back' link on 'Are you sure you want to cancel? page brings the user back'", async ({
    //   page,
    // }) => {
    //   await page.getByRole("button", { name: /Exit this form/i }).click();
    //   await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
    //   await page.getByRole("link", { name: "Back" }).click();
    //   await expect(page).toHaveURL(Paths.MUST_SUBMIT_SUBJECT_ACCESS);
    // });

    test("clicking the 'No' link on 'Are you sure you want to cancel? page brings the user back'", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Exit this form/i }).click();
      await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
      await page.locator("form#cancel-request a").click();
      await expect(page).toHaveURL(Paths.MUST_SUBMIT_SUBJECT_ACCESS);
    });
  });
});
