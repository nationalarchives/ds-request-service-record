import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

test.describe("the 'What was their date of birth?' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH);
  });

  test.describe("when first rendered", () => {
    test("has the correct heading", async ({ page }) => {
      await expect(page.locator("h1")).toHaveText(
        /What was their date of birth\?/,
      );
    });
  });

  test.describe("when submitted", () => {
    test.describe("with invalid input", () => {
      test("without any input, the correct validation message is shown", async ({
        page,
      }) => {
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page.locator(".tna-fieldset__error")).toHaveText(
          /Enter the service person's date of birth/,
        );
      });

      test("with a date before 1 January 1800, the correct validation message is shown", async ({
        page,
      }) => {
        await page.getByLabel("Day").fill("01");
        await page.getByLabel("Month").fill("01");
        await page.getByLabel("Year").fill("1799");
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page.locator(".tna-fieldset__error")).toHaveText(
          /Date of birth must be after 31 December 1799. Records prior to this date are not contained in this collection./,
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
        await expect(page.locator(".tna-fieldset__error")).toHaveText(
          /The date of birth must be in the past/,
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
          test(`with day='${day}', month='${month}', year='${year}'`, async ({
            page,
          }) => {
            await page.getByLabel("Day").fill(day);
            await page.getByLabel("Month").fill(month);
            await page.getByLabel("Year").fill(year);
            await page.getByRole("button", { name: /Continue/i }).click();
            await expect(page.locator(".tna-fieldset__error")).toHaveText(
              /What was their date of birth\? must be a real date/,
            );
          });
        }
      });
    });
    test.describe("with valid input", () => {
      const validSubmissionMappings = [
        {
          month: "01",
          day: "01",
          year: "1890",
          nextUrl: Paths.SERVICE_PERSON_DETAILS,
          heading: /Tell us as much as you know about the service person/,
          description:
            "when the year of birth is 1890, the 'Tell us as much as you know about the service person' page is shown and any 'Back' links work as expected",
        },
        {
          month: "01",
          day: "01",
          year: "1950",
          nextUrl: Paths.WE_DO_NOT_HAVE_RECORDS_FOR_PEOPLE_BORN_AFTER,
          heading: /We do not have records for people born after 1939/,
          description:
            "when the year of birth is 1950, the 'We do not have records for people born after 1939' page is shown and any 'Back' links work as expected",
        },
        {
          month: "01",
          day: "01",
          year: "1925",
          nextUrl: Paths.DO_YOU_HAVE_A_PROOF_OF_DEATH,
          heading: /Provide a proof of death/,
          description:
            "when the year of birth is 1925, the 'Provide proof of death' page is shown and any 'Back' links work as expected",
        },
      ];

      validSubmissionMappings.forEach(
        ({ day, month, year, nextUrl, heading, description }) => {
          test(description, async ({ page }) => {
            await page.getByLabel("Day").fill(day);
            await page.getByLabel("Month").fill(month);
            await page.getByLabel("Year").fill(year);
            await page.getByRole("button", { name: /Continue/i }).click();
            await expect(page).toHaveURL(nextUrl);
            await expect(page.locator("h1")).toHaveText(heading);
            // const backLink = page.getByRole("link", { name: "Back" });
            // // If there's a "Back" link, click it
            // if ((await backLink.count()) > 0) {
            //   await backLink.click();
            //   await expect(page).toHaveURL(Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH);
            // }
          });
        },
      );
    });
  });
});
