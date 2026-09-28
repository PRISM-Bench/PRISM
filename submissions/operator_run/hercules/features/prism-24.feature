Feature: PRISM-24
  Scenario: PRISM-24
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-24
    When Add your signature to the agreement.
    Then A confirmation that the signature was recorded is shown.
