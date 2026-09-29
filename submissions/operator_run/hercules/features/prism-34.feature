Feature: PRISM-34
  Scenario: PRISM-34
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-34
    When Buy the asset the page asks for, then confirm the purchase.
    Then A confirmation that the purchase succeeded is shown.
