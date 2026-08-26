import { test, expect } from "@playwright/test";

test.describe("Checking the execution context", () => {
  test("MOCK_S3 is enabled in CI", async () => {
    if (process.env.CI) {
      expect(process.env.MOCK_S3).toBe("true");
    }
  });
});
