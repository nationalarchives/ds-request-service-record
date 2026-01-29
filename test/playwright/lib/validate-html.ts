import { test, expect, Page } from "@playwright/test";
import { HtmlValidate, ConfigData } from "html-validate";

const config: ConfigData = {
  extends: ["html-validate:recommended"],
  rules: {
    "attribute-empty-style": ["off", { style: "omit" }],
    "attribute-boolean-style": ["off", { style: "omit" }],
    "no-inline-style": "warn", // video.js
    "no-trailing-whitespace": "off",
    "prefer-native-element": "warn", // video.js
    "script-type": "off",
    "long-title": ["error", { maxlength: 85 }], // Adjusted to accommodate some longer title lengths (See commit)
  },
};

const htmlvalidate = new HtmlValidate(config);

const validateHtml: (page: Page) => void = async (page) => {
  await test.step("Validate HTML", async () => {
    const html = await page.content();
    const report = await htmlvalidate.validateString(html);

    const errors =
      report.results[0]?.messages.filter((message) => message.severity === 2) ||
      [];
    await expect(errors).toEqual([]);

    const warnings =
      report.results[0]?.messages.filter((message) => message.severity === 1) ||
      [];
    if (report.warningCount) {
      console.log(`${report.warningCount} warnings`);
      warnings.forEach((message) => {
        console.log(message);
      });
    }
    await expect(report.warningCount).toBeLessThanOrEqual(3);

    await expect(report.valid).toBeTruthy();
  });
};

export default validateHtml;
