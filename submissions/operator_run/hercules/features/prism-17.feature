Feature: PRISM-17
  Scenario: PRISM-17
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-17
    When Confirm the order.
    Then A confirmation that the order succeeded is shown.
