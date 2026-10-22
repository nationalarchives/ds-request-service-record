import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import {
  clickBackLink,
  continueFromChooseYourOrderType,
  continueFromWhatWasTheirDateOfBirth,
} from "../lib/step-functions";
import { checkForProofOfDeathWarning } from "../lib/check-for-proof-of-death-warning";

const orderCases = [
  {
    label: "99 years ago",
    year: String(new Date().getFullYear() - 99),
    orderType: "Choose standard",
    expectedNextPath: Paths.PROVIDE_A_PROOF_OF_DEATH,
  },
  {
    label: "99 years ago",
    year: String(new Date().getFullYear() - 99),
    orderType: "Choose full record check",
    expectedNextPath: Paths.PROVIDE_A_PROOF_OF_DEATH,
  },
  {
    label: "101 years ago",
    year: String(new Date().getFullYear() - 101),
    orderType: "Choose standard",
    expectedNextPath: Paths.YOUR_CONTACT_DETAILS,
  },
  {
    label: "101 years ago",
    year: String(new Date().getFullYear() - 101),
    orderType: "Choose full record check",
    expectedNextPath: Paths.PROVIDE_A_PROOF_OF_DEATH,
  },
  {
    label: "115 years ago",
    year: String(new Date().getFullYear() - 115),
    orderType: "Choose standard",
    expectedNextPath: Paths.YOUR_CONTACT_DETAILS,
  },
  {
    label: "115 years ago",
    year: String(new Date().getFullYear() - 115),
    orderType: "Choose full record check",
    expectedNextPath: Paths.PROVIDE_A_PROOF_OF_DEATH,
  },
  {
    label: "116 years ago",
    year: String(new Date().getFullYear() - 116),
    orderType: "Choose standard",
    expectedNextPath: Paths.YOUR_CONTACT_DETAILS,
  },
  {
    label: "116 years ago",
    year: String(new Date().getFullYear() - 116),
    orderType: "Choose full record check",
    expectedNextPath: Paths.YOUR_CONTACT_DETAILS,
  },
];

const warningCases = [
  {
    label: "99 years ago",
    year: String(new Date().getFullYear() - 99),
    shouldSeeWarning: false,
  },
  {
    label: "101 years ago",
    year: String(new Date().getFullYear() - 101),
    shouldSeeWarning: true,
  },
  {
    label: "115 years ago",
    year: String(new Date().getFullYear() - 115),
    shouldSeeWarning: true,
  },
  {
    label: "116 years ago",
    year: String(new Date().getFullYear() - 116),
    shouldSeeWarning: false,
  },
];

test.describe("choose your order type", () => {
  warningCases.forEach(({ label, year, shouldSeeWarning }) => {
    test(`when the service person was born ${label}, the proof of death warning is ${shouldSeeWarning ? "visible" : "hidden"}`, async ({
      page,
    }) => {
      await page.goto(Paths.JOURNEY_START);
      await page.goto(Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH);
      await continueFromWhatWasTheirDateOfBirth(
        page,
        "15",
        "06",
        year,
        Paths.SERVICE_PERSON_DETAILS,
        true,
        "",
      );
      await page.goto(Paths.CHOOSE_YOUR_ORDER_TYPE);

      await checkForProofOfDeathWarning(page, shouldSeeWarning);
    });
  });

  orderCases.forEach(({ label, year, orderType, expectedNextPath }) => {
    test(`when the service person was born ${label}, selecting '${orderType}' continues to '${expectedNextPath}'`, async ({
      page,
    }) => {
      await page.goto(Paths.JOURNEY_START);
      await page.goto(Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH);
      await continueFromWhatWasTheirDateOfBirth(
        page,
        "15",
        "06",
        year,
        Paths.SERVICE_PERSON_DETAILS,
        true,
        "",
      );
      await page.goto(Paths.CHOOSE_YOUR_ORDER_TYPE);

      await continueFromChooseYourOrderType(page, orderType, expectedNextPath);
    });

    test(`when the service person was born ${label}, clicking 'Back' after selecting '${orderType}' returns to 'Choose your order type'`, async ({
      page,
    }) => {
      await page.goto(Paths.JOURNEY_START);
      await page.goto(Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH);
      await continueFromWhatWasTheirDateOfBirth(
        page,
        "15",
        "06",
        year,
        Paths.SERVICE_PERSON_DETAILS,
        true,
        "",
      );
      await page.goto(Paths.CHOOSE_YOUR_ORDER_TYPE);

      await continueFromChooseYourOrderType(page, orderType, expectedNextPath);
      await clickBackLink(page, Paths.CHOOSE_YOUR_ORDER_TYPE);
    });
  });
});
