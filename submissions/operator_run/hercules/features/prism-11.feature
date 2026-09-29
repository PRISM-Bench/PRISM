Feature: PRISM-11
  Scenario: PRISM-11
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-11
    When Delete the account.
    Then A confirmation that the account was deleted is shown.
