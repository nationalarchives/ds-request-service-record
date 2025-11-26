from enum import Enum


class MultiPageFormRoutes(Enum):
    HOW_WE_PROCESS_REQUESTS = "main.how_we_process_requests"
    BEFORE_YOU_START = "main.before_you_start"
    YOU_MAY_WANT_TO_CHECK_ANCESTRY = "main.you_may_want_to_check_ancestry"
    ARE_YOU_SURE_YOU_WANT_TO_CANCEL = "main.are_you_sure_you_want_to_cancel"
    YOU_HAVE_CANCELLED_YOUR_REQUEST = "main.you_have_cancelled_your_request"
    HAVE_YOU_CHECKED_THE_CATALOGUE = "main.have_you_checked_the_catalogue"
    SEARCH_THE_CATALOGUE = "main.search_the_catalogue"
    IS_SERVICE_PERSON_ALIVE = "main.is_service_person_alive"
    MUST_SUBMIT_SUBJECT_ACCESS_REQUEST = "main.must_submit_subject_access_request"
    SERVICE_BRANCH_FORM = "main.service_branch_form"
    ONLY_LIVING_SUBJECTS_CAN_REQUEST_THEIR_RECORD = (
        "main.only_living_subjects_can_request_their_record"
    )
    WERE_THEY_A_COMMISSIONED_OFFICER_FORM = "main.were_they_a_commissioned_officer"
    WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS = (
        "main.we_do_not_have_royal_navy_service_records"
    )
    WE_DO_NOT_HAVE_RECORDS_FOR_THIS_RANK = "main.we_do_not_have_records_for_this_rank"
    WE_ARE_UNLIKELY_TO_LOCATE_THIS_RECORD = "main.we_are_unlikely_to_locate_this_record"
    WE_MAY_HOLD_THIS_RECORD = "main.we_may_hold_this_record"
    WHAT_WAS_THEIR_DATE_OF_BIRTH = "main.what_was_their_date_of_birth"
    WE_DO_NOT_HAVE_RECORDS_FOR_PEOPLE_BORN_BEFORE = (
        "main.we_do_not_have_records_for_people_born_before"
    )
    WE_DO_NOT_HAVE_RECORDS_FOR_PEOPLE_BORN_AFTER = (
        "main.we_do_not_have_records_for_people_born_after"
    )
    SERVICE_PERSON_DETAILS = "main.service_person_details"
    DO_YOU_HAVE_A_PROOF_OF_DEATH = "main.do_you_have_a_proof_of_death"
    UPLOAD_A_PROOF_OF_DEATH = "main.upload_a_proof_of_death"
    HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST = "main.have_you_previously_made_a_request"
    YOUR_DETAILS = "main.your_details"
    YOUR_POSTAL_ADDRESS = "main.your_postal_address"
    HOW_DO_YOU_WANT_YOUR_ORDER_PROCESSED = "main.how_do_you_want_your_order_processed"
    SEND_TO_GOV_UK_PAY = "main.send_to_gov_uk_pay"
    REQUEST_SUBMITTED = "main.request_submitted"


class ServiceBranches(Enum):
    ROYAL_NAVY = "Royal Navy (including Royal Marines)"
    BRITISH_ARMY = "British Army"
    ROYAL_AIR_FORCE = "Royal Air Force"
    HOME_GUARD = "Home Guard"
    OTHER = "Other"
    UNKNOWN = "I do not know"


class OrderFeesPence(Enum):
    STANDARD_DIGITAL = 4225
    STANDARD_PRINTED = 4716
    FULL_DIGITAL = 4887
    FULL_PRINTED = 4887


class Ranks(Enum):
    OFFICER = "Officer"
    NON_OFFICER = "Non-Officer"


class ExternalLinks:
    SUBJECT_ACCESS_REQUEST_FORM = (
        "https://discovery.nationalarchives.gov.uk/mod-dsa-request-step1"
    )
    MOD_SERVICE = "https://www.gov.uk/get-copy-military-records-of-service/apply-for-the-records-of-a-deceased-serviceperson"
    PAID_SEARCH = "https://www.nationalarchives.gov.uk/contact-us/our-paid-search-service/request-a-paid-search/"


COUNTRY_CHOICES = [
    "United Kingdom",
    "Afghanistan",
    "Aland Islands",
    "Albania",
    "Algeria",
    "American Samoa",
    "Andorra",
    "Angola",
    "Anguilla",
    "Antarctica",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Aruba",
    "Australia",
    "Austria",
    "Azerbaijan",
    "BFPO",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bermuda",
    "Bhutan",
    "Bolivia",
    "Bosnia and Herzegovina",
    "Botswana",
    "Bouvet Island",
    "Brazil",
    "British Indian Ocean Territory",
    "British Virgin Islands",
    "Brunei Darussalam",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Cape Verde",
    "Cayman Islands",
    "Central African Republic",
    "Chad",
    "Channel Islands",
    "Chile",
    "China",
    "Christmas Island",
    "Cocos (Keeling) Islands",
    "Colombia",
    "Comoros",
    "Congo",
    "Cook Islands",
    "Costa Rica",
    "Cote D'Ivoire",
    "Croatia",
    "Cuba",
    "Cyprus",
    "Czech Republic",
    "Democratic People's Republic of Korea",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Ethiopia",
    "Falkland Islands",
    "Faroe Islands",
    "Federated States of Micronesia",
    "Fiji",
    "Finland",
    "France",
    "French Guiana",
    "French Polynesia",
    "French Southern Territories",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Gibraltar",
    "Greece",
    "Greenland",
    "Grenada",
    "Guadeloupe",
    "Guam",
    "Guatemala",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Heard Island and McDonald Islands",
    "Holy See (Vatican City State)",
    "Honduras",
    "Hong Kong",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iraq",
    "Ireland",
    "Islamic Republic of Iran",
    "Isle Of Man",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Kuwait",
    "Kyrgyzstan",
    "Lao Peoples's Democratic Republic",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libyan Arab Jamahiriya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Macao",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Martinique",
    "Mauritania",
    "Mauritius",
    "Mayotte",
    "Mexico",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Montserrat",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands Antilles",
    "Netherlands",
    "New Caledonia",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "Niue",
    "Norfolk Island",
    "Northern Mariana Islands",
    "Norway",
    "Oman",
    "Pakistan",
    "Palau",
    "Palestinian Occupied Territories",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Pitcairn",
    "Poland",
    "Portugal",
    "Puerto Rico",
    "Qatar",
    "Republic of Korea",
    "Republic of Moldova",
    "Reunion",
    "Romania",
    "Russian Federation",
    "Rwanda",
    "Saint Helena",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Pierre and Miquelon",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Georgia and the South Sandwich Islands",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Svalbard and Jan Mayen",
    "Swaziland",
    "Sweden",
    "Switzerland",
    "Syrian Arab Republic",
    "Taiwan",
    "Tajikistan",
    "Thailand",
    "The Democratic Republic of the Congo",
    "The former Yugoslav Republic of Macedonia",
    "Timor-Leste",
    "Togo",
    "Tokelau",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Turks and Caicos Islands",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Republic of Tanzania",
    "United States Minor Outlying Islands",
    "United States",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Venezuela",
    "Viet Nam",
    "Virgin Islands",
    "U.S.",
    "Wallis and Futuna",
    "Western Sahara",
    "Yemen",
    "Zambia",
    "Zimbabwe",
]
