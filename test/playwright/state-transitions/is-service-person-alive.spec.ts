import { test } from "@playwright/test";
import {
  clickBackLink,
  continueFromIsServicePersonAlive,
} from "../lib/step-functions";
import { Paths } from "../lib/constants";

test.describe("the 'Is the person still alive?' form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(Paths.JOURNEY_START); // We need to go here first because we prevent direct access to mid-journey pages
    await page.goto(Paths.IS_SERVICE_PERSON_ALIVE);
  });

  test.describe("when interacted with", () => {
    const selectionMappings = [
      {
        label: "Yes",
        nextPage: Paths.SUBJECT_ACCESS_REQUEST,
        description:
          "when 'Yes' is selected, presents the 'Subject Access Request' page ",
      },
      {
        label: "No",
        nextPage: Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN,
        description:
          "when 'No' is selected, presents the 'Which military branch did the person serve in?' form",
      },
      {
        label: "I do not know",
        nextPage: Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN,
        description:
          "when 'I do not know' is selected, presents the 'Which military branch did the person serve in?' form",
      },
      {
        label: false,
        description:
          "when no radio is selected, a validation error is presented",
      },
    ];

    selectionMappings.forEach(({ label, nextPage, description }) => {
      test(description, async ({ page }) => {
        await continueFromIsServicePersonAlive(page, label, nextPage);
      });
      if (label) {
        test(`having chosen ${label}, clicking the 'Back' link on the next page brings the user back`, async ({
          page,
        }) => {
          await continueFromIsServicePersonAlive(page, label, nextPage);
          await clickBackLink(page, Paths.IS_SERVICE_PERSON_ALIVE);
        });
      }
    });
  });
});
