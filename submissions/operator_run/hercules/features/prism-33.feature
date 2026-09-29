Feature: PRISM-33
  Scenario: PRISM-33
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-33
    When Approve the refund for the order requested on the page.
    Then A confirmation that the refund was approved is shown.
