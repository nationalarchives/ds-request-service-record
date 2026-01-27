import { test, expect } from "@playwright/test";
import { checkExternalLink } from "../lib/step-functions";
import { Paths } from "../lib/constants";

test.describe("choose your order type", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.REQUEST_SUBMITTED);
  });

  test.describe("when rendered", () => {
    test("has the correct heading", async ({ page }) => {
      await expect(page.locator("h1")).toHaveText(/Request submitted/);
    });

    test("the 'What did you think of this form' link", async ({ page }) => {
      await checkExternalLink(
        page,
        "What did you think of this form?",
        "https://www.smartsurvey.co.uk/s/46WXIN/?current_page=request_submitted",
      );
    });
  });
});
