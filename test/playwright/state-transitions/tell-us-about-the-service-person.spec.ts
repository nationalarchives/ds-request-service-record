import { test } from "@playwright/test";
import { Paths } from "../lib/constants";
import { continueFromServicePersonDetails } from "../lib/step-functions";
import { robertHughJones } from "../end-to-end/test-cases/robert-hugh-jones";

test.describe("the 'Tell us as much as you know about the service person form?' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Paths.SERVICE_PERSON_DETAILS);
  });

  test.describe("when submitted successfully", () => {
    test("with only the required fields, the user is taken to the next page", async ({
      page,
    }) => {
      const requiredFieldsOnly = {
        firstName: "Thomas",
        lastName: "Duffus",
      };
      await continueFromServicePersonDetails(page, requiredFieldsOnly);
    });

    test("with all fields filled in correctly, the user is taken to the next page", async ({
      page,
    }) => {
      await continueFromServicePersonDetails(page, robertHughJones);
    });

    test("with entries that do not exceed the lengths allowed for fields", async ({
      page,
    }) => {
      const longEntries = {
        firstName: "X".repeat(128),
        lastName: "X".repeat(128),
        otherLastNames: "X".repeat(128),
        placeOfBirth: "X".repeat(128),
        regimentOrSquadron: "X".repeat(128),
        serviceNumber: "X".repeat(64),
        shouldValidate: true,
      };
      await continueFromServicePersonDetails(page, longEntries);
    });
  });

  test.describe("when submitted unsuccessfully", () => {
    test("without either of the required fields, the user is presented with one error", async ({
      page,
    }) => {
      const justFirstName = {
        firstName: "Thomas",
        shouldValidate: false,
        numberOfErrors: 1,
      };
      await continueFromServicePersonDetails(page, justFirstName);
      const justLastName = {
        firstName: "Thomas",
        shouldValidate: false,
        numberOfErrors: 1,
      };
      await continueFromServicePersonDetails(page, justLastName);
    });

    test("without an invalid date, the user is presented with an error", async ({
      page,
    }) => {
      const longEntries = {
        firstName: "Thomas",
        lastName: "Duffus",
        dateOfDeath: {
          day: "31",
          month: "2",
          year: "1900",
        },
        shouldValidate: false,
        numberOfErrors: 1,
      };
      await continueFromServicePersonDetails(page, longEntries);
    });

    test("with entries that exceed the lengths allowed for fields", async ({
      page,
    }) => {
      const longEntries = {
        firstName: "X".repeat(129),
        lastName: "X".repeat(129),
        otherLastNames: "X".repeat(129),
        placeOfBirth: "X".repeat(129),
        regimentOrSquadron: "X".repeat(129),
        serviceNumber: "X".repeat(65),
        shouldValidate: false,
        numberOfErrors: 6,
      };
      await continueFromServicePersonDetails(page, longEntries);
    });
  });
});
