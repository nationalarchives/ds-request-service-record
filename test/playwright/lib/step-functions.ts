import { expect } from "@playwright/test";
import { Paths } from "./constants";

export async function continueFromJourneyStart(page) {
  await expect(page).toHaveURL(Paths.JOURNEY_START);
  await expect(page.locator("h1")).toHaveText(
    /Request a military service record/,
  );
  await page.getByRole("button", { name: /Continue/i }).click();
  await expect(page).toHaveURL(Paths.HOW_WE_PROCESS_REQUESTS);
  await expect(page.locator("h1")).toHaveText(/How we process requests/);
}

export async function continueFromHowWeProcessRequests(page) {
  await expect(page).toHaveURL(Paths.HOW_WE_PROCESS_REQUESTS);
  await expect(page.locator("h1")).toHaveText(/How we process requests/);
  await page.getByRole("button", { name: /Continue/i }).click();
  await expect(page).toHaveURL(Paths.BEFORE_YOU_START);
  await expect(page.locator("h1")).toHaveText(/Before you start/);
}

export async function continueFromBeforeYouStart(
  page,
  confirmsMandatoryInformation,
) {
  await expect(page).toHaveURL(Paths.BEFORE_YOU_START);
  await expect(page.locator("h1")).toHaveText(/Before you start/);
  if (confirmsMandatoryInformation) {
    await page
      .getByRole("checkbox", {
        name: /I confirm I can provide the mandatory information/i,
      })
      .check();
  }
  await page.getByRole("button", { name: /Start now/i }).click();
  if (confirmsMandatoryInformation) {
    await expect(page).toHaveURL(Paths.YOU_MAY_WANT_TO_CHECK_ANCESTRY);
  } else {
    await expect(page).toHaveURL(Paths.BEFORE_YOU_START);
    await expect(page.locator(".tna-error-summary__list")).toHaveText(
      /You must confirm you can provide the mandatory information/,
    );
  }
}

export async function continueFromYouMayWantToCheckAncestry(page) {
  await expect(page).toHaveURL(Paths.YOU_MAY_WANT_TO_CHECK_ANCESTRY);
  await expect(page.locator("h1")).toHaveText(/You may want to check Ancestry/);
  await page.getByRole("button", { name: /Continue/i }).click();
  await expect(page).toHaveURL(Paths.IS_SERVICE_PERSON_ALIVE);
  await expect(page.locator("h1")).toHaveText(/Is the service person alive/);
}

export async function continueFromIsServicePersonAlive(
  page,
  label,
  nextPage = "",
) {
  await expect(page).toHaveURL(Paths.IS_SERVICE_PERSON_ALIVE);
  await expect(page.locator("h1")).toHaveText(/Is the service person alive/);
  if (label) {
    await page.getByRole("radio", { name: label, exact: true }).check();
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page).toHaveURL(nextPage);
  } else {
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page.locator(".tna-fieldset__error")).toHaveText(
      /Tell us if the service person is alive/,
    );
  }
}

export async function continueFromAreYouSureYouWantToCancel(
  page,
  confirmCancel,
) {
  await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
  await expect(page.locator("h1")).toHaveText(
    /Are you sure you want to cancel?/,
  );
  // We can only check the "Yes" option because the routing for "No" is dynamic
  if (confirmCancel) {
    await page.getByRole("button", { name: /Yes/ }).click();
    await expect(page).toHaveURL(Paths.YOU_HAVE_CANCELLED_YOUR_REQUEST);
  }
}

export async function continueFromYouHaveCancelledYourRequest(page) {
  await expect(page).toHaveURL(Paths.YOU_HAVE_CANCELLED_YOUR_REQUEST);
  await expect(page.locator("h1")).toHaveText(
    /You have cancelled your request/,
  );
  await page.getByRole("link", { name: "Start a new request" }).click();
  await expect(page).toHaveURL(Paths.JOURNEY_START);
}

export async function continueFromSubmitDataAccessRequest(page) {
  await expect(page).toHaveURL(Paths.MUST_SUBMIT_SUBJECT_ACCESS);
  await expect(page.locator("h1")).toHaveText(/Submit a data access request/);
  await clickExitThisForm(page, "button");
}

export async function continueFromWhichMilitaryBranchDidThePersonServeIn(
  page,
  branchLabel,
  nextUrlAfterBranchSelection = "",
) {
  await expect(page).toHaveURL(
    Paths.WHICH_MILITARY_BRANCH_DID_THE_PERSON_SERVE_IN,
  );
  await expect(page.locator("h1")).toHaveText(
    /Which military branch did the person serve in\?/,
  );
  if (branchLabel) {
    await page.getByLabel(branchLabel, { exact: true }).check();
    await page.getByRole("button", { name: /Continue/i }).click();
    if (nextUrlAfterBranchSelection) {
      await expect(page).toHaveURL(nextUrlAfterBranchSelection);
    }
  } else {
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page.locator(".tna-fieldset__error")).toHaveText(
      /Select the branch they served in/,
    );
  }
}

export async function continueFromWeDoNotHaveRoyalNavyServiceRecords(page) {
  await expect(page).toHaveURL(Paths.WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS);
  await expect(page.locator("h1")).toHaveText(/We do not hold this record/);
  await clickExitThisForm(page, "button");
}

export async function continueFromWeAreUnlikelyToLocateThisRecord(page) {
  await expect(page).toHaveURL(Paths.WE_ARE_UNLIKELY_TO_LOCATE_THIS_RECORD);
  await expect(page.locator("h1")).toHaveText(
    /We are unlikely to be able to locate this record/,
  );
  await clickExitThisForm(page, "button");
}

export async function continueFromWeAreUnlikelyToHoldThisRecord(
  page,
  pathVariant,
) {
  await expect(page).toHaveURL(pathVariant);
  await expect(page.locator("h1")).toHaveText(
    /We are unlikely to hold this record/,
  );
  await clickContinueThisRequestForm(page, "button");
}

export async function continueFromWereTheyACommissionedOfficer(
  page,
  answerLabel,
  nextUrlAfterOfficerSelection,
  expectedTemplateIdentifier,
) {
  await expect(page).toHaveURL(Paths.WERE_THEY_A_COMMISSIONED_OFFICER);
  await expect(page.locator("h1")).toHaveText(
    /Were they a Commissioned Officer/,
  );
  if (answerLabel) {
    await page.getByRole("radio", { name: answerLabel, exact: true }).check();
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page).toHaveURL(nextUrlAfterOfficerSelection);
    // Because the templates in this part of the journey can be only subtly different,
    // we check for a template identifier to ensure the correct template is shown
    await expect(
      page.locator(`[data-template-id="${expectedTemplateIdentifier}"]`),
    ).toBeVisible();
  } else {
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page.locator(".tna-fieldset__error")).toHaveText(
      /Tell us if the service person was a Commissioned Officer/,
    );
  }
}

export async function continueFromWeMayHoldThisRecord(page) {
  await expect(page).toHaveURL(Paths.WE_MAY_HOLD_THIS_RECORD);
  await expect(page.locator("h1")).toHaveText(/We may hold this record/);
  await page.getByRole("button", { name: /Continue/i }).click();
  await expect(page).toHaveURL(Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH);
}

export async function continueFromWhatWasTheirDateOfBirth(
  page,
  day,
  month,
  year,
  nextUrl,
  shouldValidate = true,
  validationMessage,
) {
  await expect(page).toHaveURL(Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH);
  await expect(page.locator("h1")).toHaveText(/What was their date of birth/);
  await page.getByLabel("Day").fill(day);
  await page.getByLabel("Month").fill(month);
  await page.getByLabel("Year").fill(year);
  await page.getByRole("button", { name: /Continue/i }).click();
  if (shouldValidate) {
    await expect(page).toHaveURL(nextUrl);
  } else {
    await expect(page.locator(".tna-fieldset__error")).toHaveText(
      validationMessage,
    );
  }
}

export async function continueFromWeDoNotHaveRecordsForPeopleBornAfter(page) {
  await expect(page).toHaveURL(
    Paths.WE_DO_NOT_HAVE_RECORDS_FOR_PEOPLE_BORN_AFTER,
  );
  await expect(page.locator("h1")).toHaveText(
    /We do not have records for people born after 1939/,
  );
  await clickExitThisForm(page, "button");
}

export async function continueFromProvideAProofOfDeath(
  page,
  label,
  nextUrl,
  heading,
) {
  await expect(page).toHaveURL(Paths.PROVIDE_A_PROOF_OF_DEATH);
  await expect(page.locator("h1")).toHaveText("Provide a proof of death");
  if (label) {
    await page.getByRole("radio", { name: label, exact: true }).check();
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page).toHaveURL(nextUrl);
    await expect(page.locator("h1")).toHaveText(heading);
  } else {
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page.locator(".tna-fieldset__error")).toHaveText(
      /Tell us if you have a proof of death/,
    );
  }
}

export async function continueFromAreYouSureYouWantToProceedWithoutAProofOfDeath(
  page,
  label,
  nextUrl,
  heading,
) {
  await expect(page).toHaveURL(
    Paths.ARE_YOU_SURE_YOU_WANT_TO_PROCEED_WITHOUT_A_PROOF_OF_DEATH,
  );
  await expect(page.locator("h1")).toHaveText(
    /Are you sure you want to proceed without a proof of death?/,
  );
  if (label) {
    await page.getByRole("radio", { name: label, exact: true }).check();
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page).toHaveURL(nextUrl);
    await expect(page.locator("h1")).toHaveText(heading);
  } else {
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page.locator(".tna-fieldset__error")).toHaveText(
      /Confirm if you want to continue without providing a proof of death/,
    );
  }
}

export async function continueFromUploadAProofOfDeath(
  page,
  fileExtension,
  fileSizeInBytes,
  shouldValidate = false,
  validationMessage,
) {
  await expect(page).toHaveURL(Paths.UPLOAD_A_PROOF_OF_DEATH);
  await expect(page.locator("h1")).toHaveText(/Upload a proof of death/);
  const fileBuffer = Buffer.alloc(fileSizeInBytes);
  if (fileExtension && fileSizeInBytes) {
    await page.getByLabel("Upload a file").setInputFiles({
      name: `proof-of-death.${fileExtension}`,
      mimeType: "application/octet-stream",
      buffer: fileBuffer,
    });
  }
  await page.getByRole("button", { name: /Continue/i }).click();
  if (shouldValidate) {
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page).toHaveURL(Paths.SERVICE_PERSON_DETAILS);
  } else {
    await expect(page.locator(".tna-form-item__error")).toHaveText(
      validationMessage,
    );
  }
}

export async function continueFromServicePersonDetails(
  page,
  {
    firstName,
    lastName,
    otherLastNames,
    serviceNumber,
    placeOfBirth,
    didTheyDieInService,
    dateOfDeath,
    regimentOrSquadron,
    additionalInformation,
    shouldValidate = true,
    numberOfErrors = 0,
  }: {
    firstName?: string;
    lastName?: string;
    otherLastNames?: string;
    serviceNumber?: string;
    placeOfBirth?: string;
    didTheyDieInService?: string;
    dateOfDeath?: { day: string; month: string; year: string };
    regimentOrSquadron?: string;
    additionalInformation?: string;
    shouldValidate?: boolean;
    numberOfErrors?: number;
  },
) {
  await expect(page).toHaveURL(Paths.SERVICE_PERSON_DETAILS);
  await expect(page.locator("h1")).toHaveText(
    /Tell us as much as you know about the service person/,
  );
  if (firstName) {
    await page.getByLabel("Forenames").fill(firstName);
  }
  if (lastName) {
    await page.getByLabel("Last name", { exact: true }).fill(lastName);
  }
  if (otherLastNames) {
    await page.getByLabel("Other last names (optional)").fill(otherLastNames);
  }
  if (serviceNumber) {
    await page.getByLabel("Service number (optional)").fill(serviceNumber);
  }
  if (placeOfBirth) {
    await page.getByLabel("Place of birth (optional)").fill(placeOfBirth);
  }
  if (didTheyDieInService) {
    await page
      .getByRole("radio", { name: didTheyDieInService, exact: true })
      .check();
  }
  if (dateOfDeath) {
    if (dateOfDeath.day && dateOfDeath.month && dateOfDeath.year) {
      await page.getByLabel("Day").fill(dateOfDeath.day);
      await page.getByLabel("Month").fill(dateOfDeath.month);
      await page.getByLabel("Year").fill(dateOfDeath.year);
    }
  }
  if (regimentOrSquadron) {
    await page
      .getByLabel("Regiment or squadron (optional)")
      .fill(regimentOrSquadron);
  }
  if (additionalInformation) {
    await page
      .getByLabel("Additional information (optional)")
      .fill(additionalInformation);
  }
  await page.getByRole("button", { name: /Continue/i }).click();
  if (shouldValidate) {
    await expect(page).toHaveURL(Paths.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST);
  } else {
    await expect(page.locator(".tna-error-summary__item")).toHaveCount(
      numberOfErrors,
    );
  }
}

export async function continueFromHaveYouPreviouslyMadeARequest(
  page: any,
  label: any,
  errorMessage?: any,
  populateReferenceNumber?: any,
) {
  await expect(page).toHaveURL(Paths.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST);
  await expect(page.locator("h1")).toHaveText(
    /Have you previously made a request for this record/,
  );
  if (label) {
    await page.getByRole("radio", { name: label, exact: true }).check();
    if (populateReferenceNumber) {
      await page.getByLabel("Reference number").fill("ABC123");
    }
    await page.getByRole("button", { name: /Continue/i }).click();
    if (errorMessage) {
      await expect(page.locator(".tna-error-summary__link")).toHaveText(
        errorMessage,
      );
    } else {
      await expect(page).toHaveURL(Paths.CHOOSE_YOUR_ORDER_TYPE);
    }
  }
}

export async function continueFromChooseYourOrderType(page, buttonText) {
  await expect(page).toHaveURL(Paths.CHOOSE_YOUR_ORDER_TYPE);
  await expect(page.locator("h1")).toHaveText(/Choose your order type/);
  await page.getByRole("button", { name: buttonText }).click();
  await expect(page).toHaveURL(Paths.YOUR_CONTACT_DETAILS);
}

export async function continueFromYourContactDetails(
  page,
  personMakingRequest,
) {
  await expect(page).toHaveURL(Paths.YOUR_CONTACT_DETAILS);
  await expect(page.locator("h1")).toHaveText(/Your contact details/);
  await page.getByLabel("First name").fill(personMakingRequest.firstName);
  await page.getByLabel("Last name").fill(personMakingRequest.lastName);
  if (personMakingRequest.emailAddress) {
    await page
      .getByLabel("Email", { exact: true })
      .fill(personMakingRequest.emailAddress);
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page).toHaveURL(Paths.YOUR_ORDER_SUMMARY);
  } else {
    await page.getByLabel("I do not have an email address").check();
    await page.getByRole("button", { name: /Continue/i }).click();
    await expect(page).toHaveURL(Paths.WHAT_IS_YOUR_ADDRESS);
  }
}

export async function continueFromYourPostalAddress(page) {
  await expect(page).toHaveURL(Paths.WHAT_IS_YOUR_ADDRESS);
  await expect(page.locator("h1")).toHaveText(/What is your address/);
  await page.getByLabel("Address Line 1").fill("123 Non-existent Road");
  await page.getByLabel("Town or city").fill("Non-existent Town");
  await page.getByLabel("Postcode").fill("TW9 4DU");
  await page.getByLabel("Country").selectOption("United Kingdom");
  await page.getByRole("button", { name: /Continue/i }).click();
  await expect(page).toHaveURL(Paths.YOUR_ORDER_SUMMARY);
}

export async function continueFromPaymentIncomplete(page) {
  await expect(page).toHaveURL(Paths.PAYMENT_INCOMPLETE);
  await expect(page.locator("h1")).toHaveText(
    /Sorry, there was a problem processing your payment/,
  );
  await page
    .getByRole("button", { name: "Go back to try the payment again" })
    .click();
  await expect(page).toHaveURL(Paths.YOUR_ORDER_SUMMARY);
}

export async function checkExternalLink(page, linkText, expectedHref) {
  const link = page.getByRole("link", { name: linkText });
  await expect(link).toHaveAttribute("href", expectedHref);
  await expect(link).toHaveAttribute("target", "_blank");
}

export async function clickExitThisForm(page, element) {
  await page.getByRole(element, { name: "Exit this form" }).click();
  await expect(page).toHaveURL(Paths.ARE_YOU_SURE_YOU_WANT_TO_CANCEL);
}

export async function clickContinueThisRequestForm(page, element) {
  await page.getByRole(element, { name: "Continue this request" }).click();
  await expect(page).toHaveURL(Paths.WHAT_WAS_THEIR_DATE_OF_BIRTH);
}

export async function clickBackLink(page, expectedPath) {
  await page.getByRole("link", { name: "Back", exact: true }).click();
  await expect(page).toHaveURL(expectedPath);
}
