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

  test("clicking the 'Back' link takes the user to the 'Is the service person alive? page'", async ({
    page,
  }) => {
    await page.getByRole("link", { name: "Back" }).click();
    await expect(page).toHaveURL(Paths.IS_SERVICE_PERSON_ALIVE);
  });

  test.describe("'Submit a data access request' link", () => {
    test("has the correct destination and is set to open in new tab", async ({
      page,
    }) => {
      const link = page.getByRole("link", {
        name: "Submit a data access request",
      });
      await expect(link).toHaveAttribute(
        "href",
        "https://discovery.nationalarchives.gov.uk/mod-dsa-request-step1",
      );
      await expect(link).toHaveAttribute("target", "_blank");
    });
  });

  test.describe("'Exit this form' and 'Back' links", () => {
    test("clicking the 'Exit this form' button takes the user to 'Are you sure you want to cancel?'", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Exit this form/i }).click();
      await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
    });

    test("clicking the 'Back' link on 'Are you sure you want to cancel? page brings the user back'", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Exit this form/i }).click();
      await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Paths.MUST_SUBMIT_SUBJECT_ACCESS);
    });

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
