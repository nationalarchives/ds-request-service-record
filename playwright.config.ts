import { defineConfig, devices } from "@playwright/test";

export const cookiePreferencesSetKey = "dontShowCookieNotice";

export default defineConfig({
  testDir: "./test/playwright",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: 2,
  workers: process.env.CI ? 1 : undefined,
  timeout: process.env.CI ? 30000 : 5000,
  reporter: process.env.CI
    ? [
        ["dot"],
        ["@estruyf/github-actions-reporter"],
        ["json", { outputFile: "test-results.json" }],
      ]
    : "line",
  use: {
    baseURL: "http://localhost:65517",
    trace: "on-first-retry",
  },
  snapshotPathTemplate:
    "{testDir}/{testFilePath}-snapshots/{arg}-{projectName}{ext}",
  expect: {
    toHaveScreenshot: {
      pathTemplate:
        "{testDir}/{testFilePath}-snapshots/{arg}-{projectName}-{platform}{ext}",
    },
    toMatchAriaSnapshot: {
      pathTemplate:
        "{testDir}/{testFilePath}-snapshots/{arg}-{projectName}{ext}",
    },
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] },
    },
    {
      name: "webkit",
      use: { ...devices["Desktop Safari"] },
    },
    {
      name: "Mobile Chrome",
      use: { ...devices["Pixel 7"] },
    },
    {
      name: "Mobile Safari",
      use: { ...devices["iPhone 15"] },
    },
  ],
});
