Feature: PRISM-28
  Scenario: PRISM-28
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-28
    When Approve the order in the Active orders list.
    Then A confirmation that the order was approved is shown.
