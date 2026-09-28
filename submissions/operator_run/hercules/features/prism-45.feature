Feature: PRISM-45
  Scenario: PRISM-45
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-45
    When Confirm the order.
    Then A confirmation that the order succeeded is shown.
