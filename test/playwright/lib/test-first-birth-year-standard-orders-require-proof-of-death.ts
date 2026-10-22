import { expect } from "@playwright/test";

export async function testfirstBirthYearStandardOrdersRequireProofOfDeath(
  page,
) {
  const firstBirthYearStandardOrdersRequireProofOfDeath = String(
    new Date().getFullYear() - 100,
  );
  const rows = page.locator(
    "[data-first-birth-year-standard-orders-require-proof-of-death]",
  );
  await expect(rows.first()).toBeVisible();
  for (const row of await rows.all()) {
    await expect(row).toHaveText(
      firstBirthYearStandardOrdersRequireProofOfDeath,
    );
  }
}
