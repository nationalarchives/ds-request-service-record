import { expect } from "@playwright/test";

export async function testLastBirthYearForOpenRecords(page) {
  const lastBirthYearForOpenRecords = String(
    new Date().getFullYear() - (115 + 1),
  );
  for (const row of await page
    .locator("[data-last-birth-year-for-open-records]")
    .all()) {
    await expect(row).toHaveText(lastBirthYearForOpenRecords);
  }
}
