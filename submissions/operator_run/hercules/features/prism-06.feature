Feature: PRISM-06
  Scenario: PRISM-06
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-06
    When Confirm the order.
    Then A confirmation that the order was confirmed is shown.
