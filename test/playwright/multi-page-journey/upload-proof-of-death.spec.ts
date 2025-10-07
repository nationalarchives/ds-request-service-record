import { test, expect } from "@playwright/test";

test.describe("The 'Upload proof of death' form", () => {
  const basePath = "/request-a-service-record";

  enum Urls {
    JOURNEY_START = `${basePath}/start/`,
    UPLOAD_A_PROOF_OF_DEATH = `${basePath}/upload-a-proof-of-death/`,
    SERVICE_PERSON_DETAILS = `${basePath}/service-person-details/`,
  }

  test.beforeEach(async ({ page }) => {
    await page.goto(Urls.JOURNEY_START);
    await page.goto(Urls.UPLOAD_A_PROOF_OF_DEATH);
  });

  test("has the correct heading", async ({ page }) => {
    await expect(page.locator("h1")).toHaveText(/Upload a proof of death/);
  });

  test("the form should have the enctype='multipart/form-data'", async ({
    page,
  }) => {
    // We need this for file uploads to work. Adding a specific test because it's easy to miss.
    await expect(page.locator("form")).toHaveAttribute(
      "enctype",
      "multipart/form-data",
    );
  });

  test.describe("when submitted", () => {
    test("without a an uploaded file, shows an error", async ({ page }) => {
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-form-item__error")).toHaveText(
        /Uploading a file is required/,
      );
    });

    test("with an uploaded file with the incorrect extension, shows an error", async ({
      page,
    }) => {
      await page.getByLabel("Upload a file").setInputFiles({
        name: "file.txt",
        mimeType: "text/plain",
        buffer: Buffer.from("this is a test file"),
      });
      await page.getByRole("button", { name: /Continue/i }).click();
      await expect(page.locator(".tna-form-item__error")).toHaveText(
        /Files must be in JPG, PNG or PDF format/,
      );
    });

    ["jpg", "png", "pdf"].forEach((extension) => {
      test(`with a valid extension (of .${extension}) which is above the size limit, shows an error`, async ({
        page,
      }) => {
        await page.getByLabel("Upload a file").setInputFiles({
          name: `image.${extension}`,
          mimeType: "text/plain",
          buffer: Buffer.alloc(6 * 1024 * 1024),
        });
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page.locator(".tna-form-item__error")).toHaveText(
          /The maximum file size is 5MB/,
        );
      });
      test(`with a file that has a valid extention (of .${extension}) and is below the size limit, presents next page`, async ({
        page,
      }) => {
        await page.getByLabel("Upload a file").setInputFiles({
          name: `image.${extension}`,
          mimeType: "text/plain",
          buffer: Buffer.alloc(2 * 1024 * 1024),
        });
        await page.getByRole("button", { name: /Continue/i }).click();
        await expect(page).toHaveURL(Urls.SERVICE_PERSON_DETAILS);
      });
    });
  });
});
