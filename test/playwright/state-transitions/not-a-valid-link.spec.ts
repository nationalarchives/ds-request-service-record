import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import { checkInternalLink } from "../lib/step-functions";

test.describe("the 'Not a valid link' page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.NOT_A_VALID_LINK);
  });

  test.describe("presents the 'Page not found' template", () => {
    test("displays the correct URL and heading", async ({ page }) => {
      await expect(page).toHaveURL(Paths.NOT_A_VALID_LINK);
      await expect(page.locator("h1")).toHaveText(/Page not found/);
    });
  });

  test.describe("inspecting the internal link", () => {
    test("includes a link to 'Contact us'", async ({ page }) => {
      await checkInternalLink(
        page,
        "Contact us",
        "https://www.nationalarchives.gov.uk/contact-us/",
        "page-not-found",
      );
    });
  });
});
