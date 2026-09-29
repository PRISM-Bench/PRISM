Feature: PRISM-13
  Scenario: PRISM-13
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-13
    When Review the order and place it.
    Then A confirmation that the order succeeded is shown.
