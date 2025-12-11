import { test, expect } from "@playwright/test";

test.describe("accessing mid-journey pages requirements", () => {
  const INDEX_URL = "/request-a-military-service-record/";
  const PROTECTED_URL =
    "/request-a-military-service-record/which-military-branch-did-the-person-serve-in/";

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

  test("when a user has been redirected once, they are not redirected again", async ({
    page,
  }) => {
    // The first visit to the protected route should redirect to the index route
    await page.goto(PROTECTED_URL);
    expect(page.url()).toContain(INDEX_URL);

    // Second visit to the protected route should not redirect again
    const response = await page.goto(PROTECTED_URL);

    expect(page.url()).toContain(PROTECTED_URL);
    expect(response.status()).toBe(200);
  });
});
