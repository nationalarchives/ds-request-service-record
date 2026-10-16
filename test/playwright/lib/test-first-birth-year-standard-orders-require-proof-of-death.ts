import { expect } from "@playwright/test";

export async function testfirstBirthYearStandardOrdersRequireProofOfDeath(
  page,
) {
  const firstBirthYearStandardOrdersRequireProofOfDeath = String(
    new Date().getFullYear() - 100,
  );
  for (const row of await page
    .locator("[data-first-birth-year-standard-orders-require-proof-of-death]")
    .all()) {
    await expect(row).toHaveText(
      firstBirthYearStandardOrdersRequireProofOfDeath,
    );
  }
}
