import { expect } from "@playwright/test";

export async function checkForProofOfDeathWarning(page, shouldBeVisible) {
  const proofOfDeathWarning = page.locator(
    '[data-testid="conditionally-available-warning"]',
  );
  if (shouldBeVisible) {
    await expect(proofOfDeathWarning).toBeVisible();
  } else {
    await expect(proofOfDeathWarning).not.toBeVisible();
  }
}
