Feature: PRISM-50
  Scenario: PRISM-50
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-50
    When Delete the user.
    Then A confirmation that the user was deleted is shown.
