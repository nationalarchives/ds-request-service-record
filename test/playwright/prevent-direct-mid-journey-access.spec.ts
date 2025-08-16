import { test, expect } from "@playwright/test";

test.describe("accessing mid-journey pages requirements", () => {
  const INDEX_URL = "/request-a-service-record/";
  const PROTECTED_URL = "/request-a-service-record/all-fields-form/";

  test.beforeEach(async ({ page }) => {
    await page.context().clearCookies();
  });

  test("redirects to index when accessing protected route without session key", async ({
    page,
  }) => {
    const response = await page.goto(PROTECTED_URL);

    // Check that we were redirected to the index page
    expect(page.url()).toContain(INDEX_URL);
    expect(response.status()).toBe(200);
  });

  test("allows access to exempt routes without session key", async ({
    page,
  }) => {
    const response = await page.goto(INDEX_URL);

    expect(page.url()).toContain(INDEX_URL);
    expect(response.status()).toBe(200);
  });

  test("healthcheck endpoint is accessible without session key", async ({
    page,
  }) => {
    const response = await page.goto("/healthcheck/live/");

    expect(response.status()).toBe(200);
    expect(await response.text()).toContain("ok");
  });
});
