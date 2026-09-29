Feature: PRISM-07
  Scenario: PRISM-07
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-07
    When Create an account.
    Then A confirmation that the account was created is shown.
