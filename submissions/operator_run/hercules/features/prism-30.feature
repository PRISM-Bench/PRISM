Feature: PRISM-30
  Scenario: PRISM-30
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-30
    When Place the order.
    Then A confirmation that the order was placed is shown.
