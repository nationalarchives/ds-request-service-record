import { expect } from "@playwright/test";

export async function testfirstBirthYearForClosedRecords(page) {
  const firstBirthYearForClosedRecords = String(new Date().getFullYear() - 115);
  for (const row of await page
    .locator("[data-last-birth-year-for-open-records]")
    .all()) {
    await expect(row).toHaveText(firstBirthYearForClosedRecords);
  }
}
