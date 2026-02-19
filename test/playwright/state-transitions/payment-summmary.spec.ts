import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the second payment summary page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.PAYMENT_SUMMARY);
  });

  test("renders with the correct heading", async ({ page }) => {
    await expect(
      page.getByRole("heading", { name: "Payment summary" }),
    ).toBeVisible();
  });
});
