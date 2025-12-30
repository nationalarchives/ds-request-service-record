import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  checkExternalLink,
  clickBackLink,
  continueFromYouMayWantToCheckAncestry,
} from "../lib/step-functions";

test.describe("the 'You may want to check ancestry' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.YOU_MAY_WANT_TO_CHECK_ANCESTRY);
  });

  test("works as expected", async ({ page }) => {
    await continueFromYouMayWantToCheckAncestry(page);
  });

  test("clicking the 'Back' link on the next page brings the user back", async ({
    page,
  }) => {
    await continueFromYouMayWantToCheckAncestry(page);
    await clickBackLink(page, Paths.YOU_MAY_WANT_TO_CHECK_ANCESTRY);
  });

  test("clicking the 'Search Ancestry (opens in new tab)' link opens link in new tab", async ({
    page,
  }) => {
    await checkExternalLink(
      page,
      "Search Ancestry (opens in new tab)",
      "https://www.ancestry.co.uk/search/",
    );
  });
});
