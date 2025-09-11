import { test, expect } from "@playwright/test";

test.describe("the 'What was their date of birth?' form", () => {
  const basePath = "/request-a-service-record";

  enum Urls {
    JOURNEY_START_PAGE = `${basePath}/start/`,
    WHAT_WAS_THEIR_DATE_OF_BIRTH = `${basePath}/what-was-their-date-of-birth/`,
  }

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.JOURNEY_START_PAGE); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Urls.WHAT_WAS_THEIR_DATE_OF_BIRTH);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(
      /What was their date of birth\?/,
    );
  });

  test.describe("when submitted", () => {
    test("without any input, the correct validation message is shown", async ({
      page,
    }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-form__error-message")).toHaveText(
        /The service person's date of birth is required/,
      );
    });

    test("with a date in the future, the correct validation message is shown", async ({
      page,
    }) => {
      const nextYear = (new Date().getFullYear() + 1).toString();

      await page.getByLabel("Day").fill("01");
      await page.getByLabel("Month").fill("01");
      await page.getByLabel("Year").fill(nextYear);
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-form__error-message")).toHaveText(
        /The service person's date of birth must be in the past/,
      );
    });

test.describe("with invalid dates, the correct validation message is shown", () => {
  const invalidDates = [
    { day: "31", month: "02", year: "2000" },
    { day: "00", month: "01", year: "2000" },
    { day: "15", month: "13", year: "2000" },
    { day: "aa", month: "bb", year: "cccc" },
  ];

  for (const { day, month, year } of invalidDates) {
    test(`with day='${day}', month='${month}', year='${year}'`, async ({ page }) => {
      await page.getByLabel("Day").fill(day);
      await page.getByLabel("Month").fill(month);
      await page.getByLabel("Year").fill(year);
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-form__error-message")).toHaveText(/must be a real date/);
    });
  }
});
  });
});
