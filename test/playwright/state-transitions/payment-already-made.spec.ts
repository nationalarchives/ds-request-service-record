import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";
import { checkInternalLink } from "../lib/step-functions";

test.describe("the 'Payment already made' page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.PAYMENT_ALREADY_MADE);
  });

  test.describe("presents the 'Payment already made' template", () => {
    test("displays the correct URL and heading", async ({ page }) => {
      await expect(page).toHaveURL(Paths.PAYMENT_ALREADY_MADE);
      await expect(page.locator("h1")).toHaveText(
        /Your payment was successful/,
      );
    });
  });

  test.describe("inspecting the internal link", () => {
    test("includes a link to 'Contact us'", async ({ page }) => {
      await checkInternalLink(
        page,
        "Contact us",
        "https://www.nationalarchives.gov.uk/contact-us/",
        "payment-already-made",
      );
    });
  });
});
