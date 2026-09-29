Feature: PRISM-16
  Scenario: PRISM-16
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-16
    When Open the Edit control on the account settings row that has one.
    Then A confirmation that the action succeeded is shown.
