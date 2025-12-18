import { test, expect } from "@playwright/test";
import { Paths } from "../lib/constants";

async function fillContactDetails(page, hasEmail = false) {
  await page.getByLabel("First name").fill("Joe");
  await page.getByLabel("Last name").fill("Bloggs");

  if (hasEmail) {
    await page.locator("#requester_email").fill("test@example.com");
  } else {
    await page.getByLabel("I do not have an email address").check();
  }

  await page.getByRole("button", { name: /Continue/i }).click();
}

async function fillPostalAddress(page) {
  await page.getByLabel("Address line 1").fill("123 Non-existent Road");
  await page.getByLabel("Town or city").fill("Non-existent Town");
  await page.getByLabel("Postcode").fill("TW9 4DU");
  await page.getByLabel("Country").selectOption("United Kingdom");
  await page.getByRole("button", { name: /Continue/i }).click();
}

async function selectOrderType(page, orderType: "standard" | "full") {
  const buttonName =
    orderType === "standard" ? /Choose standard/i : /Choose full record check/i;
  await page.getByRole("button", { name: buttonName }).click();
}

async function completeOrderToSummary(
  page,
  orderType: "standard" | "full",
  hasEmail = false,
) {
  await expect(page.locator("h1")).toHaveText(/Choose your order type/);
  await selectOrderType(page, orderType);
  await expect(page).toHaveURL(Paths.YOUR_CONTACT_DETAILS);
  await fillContactDetails(page, hasEmail);

  if (!hasEmail) {
    await expect(page).toHaveURL(Paths.WHAT_IS_YOUR_ADDRESS);
    await fillPostalAddress(page);
  }

  await expect(page).toHaveURL(Paths.YOUR_ORDER_SUMMARY);
}

test.describe("Routes to 'Your order summary'", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START);
    await page.goto(Paths.CHOOSE_YOUR_ORDER_TYPE);
  });

  const providedByPostTests = [
    {
      orderType: "standard" as const,
      price: "£47.16",
      description: "Standard",
    },
    {
      orderType: "full" as const,
      price: "£48.87",
      description: "Full record check",
    },
  ];

  for (const { orderType, price, description } of providedByPostTests) {
    test(`we're presenting the correct information for a ${description.toLowerCase()} order provided by post`, async ({
      page,
    }) => {
      await completeOrderToSummary(page, orderType, false);
      await expect(page.locator("#processing-option")).toHaveText(
        new RegExp(description),
      );
      await expect(page.locator("#price")).toHaveText(new RegExp(price));
      await expect(page.locator("#price")).toHaveText(
        /plus £1.04 per page copying fee/,
      );
    });
  }

  const providedByEmailTests = [
    {
      orderType: "standard" as const,
      price: "£42.25",
      description: "Standard",
    },
    {
      orderType: "full" as const,
      price: "£48.87",
      description: "Full record check",
    },
  ];

  for (const { orderType, price, description } of providedByEmailTests) {
    test(`we're presenting the correct information for a ${description.toLowerCase()} order provided by email`, async ({
      page,
    }) => {
      await completeOrderToSummary(page, orderType, true);
      await expect(page.locator("#processing-option")).toHaveText(
        new RegExp(description),
      );
      await expect(page.locator("#price")).toHaveText(new RegExp(price));
    });
  }

  test.describe("when interacted with", () => {
    test.beforeEach(async ({ page }) => {
      await completeOrderToSummary(page, "standard", false);
    });

    test.describe("the 'Change order' link", () => {
      test("takes the user to the 'Choose your order type' page", async ({
        page,
      }) => {
        await page.getByRole("link", { name: "Change order" }).click();
        await expect(page).toHaveURL(Paths.CHOOSE_YOUR_ORDER_TYPE);
      });
    });
  });
  test.describe("the 'Back' links function as expected", () => {
    test("when the user has provided an email address", async ({ page }) => {
      await selectOrderType(page, "standard");
      await fillContactDetails(page, true);
      await expect(page).toHaveURL(Paths.YOUR_ORDER_SUMMARY);
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Paths.YOUR_CONTACT_DETAILS);
    });
    test("when the user has provided a postal address", async ({ page }) => {
      await selectOrderType(page, "standard");
      await fillContactDetails(page, false);
      await fillPostalAddress(page);
      await expect(page).toHaveURL(Paths.YOUR_ORDER_SUMMARY);
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Paths.WHAT_IS_YOUR_ADDRESS);
      await page.getByRole("link", { name: "Back" }).click();
      await expect(page).toHaveURL(Paths.YOUR_CONTACT_DETAILS);
    });
  });
});
