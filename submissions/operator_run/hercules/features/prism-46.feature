Feature: PRISM-46
  Scenario: PRISM-46
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-46
    When Pick something from the catalog and buy it.
    Then A confirmation that the purchase succeeded is shown.
