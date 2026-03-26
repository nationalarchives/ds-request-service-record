import { expect } from "@playwright/test";

export async function checkContentGroupMetaTag(page) {
  const meta = page.locator(`meta[name="tna_root:content_group"]`);
  await expect(meta).toHaveCount(1);

  const contentAttribute = await meta.getAttribute("content");
  expect(contentAttribute).toContain("Request a military service");
}

export async function checkPageTypeMetaTag(page) {
  const meta = page.locator(`meta[name="tna_root:page_type"]`);
  await expect(meta).toHaveCount(1);

  const contentAttribute = await meta.getAttribute("content");
  expect(contentAttribute).toContain("_ramsr");
}
