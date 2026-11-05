import { expect } from "@playwright/test";

export async function testfirstBirthYearForClosedRecords(page) {
  const firstBirthYearForClosedRecords = String(new Date().getFullYear() - 115);
  for (const row of await page
    .locator("[data-first-birth-year-for-closed-records]")
    .all()) {
    await expect(row).toHaveText(firstBirthYearForClosedRecords);
  }
}
