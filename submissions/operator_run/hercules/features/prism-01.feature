Feature: PRISM-01
  Scenario: PRISM-01
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-01
    When Submit the transaction.
    Then A confirmation that the transaction succeeded is shown.
