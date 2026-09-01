import {test, expect} from "@playwright/test";

test.describe("Checking the environment context", () => {
    // We need MOCK_S3 because it's used in the backend logic to
    // determine whether a real or mock S3 backend is used. If Playwright
    // tests were to run without a mock S3 backend, users would be presented
    // with a "Sorry, we were unable to upload your file" page
    test("MOCK_S3 is enabled as necessary for dev and CI environments", async () => {
        if (process.env.CI) {
            expect(process.env.MOCK_S3).toBe("true");
        }
    });
});
