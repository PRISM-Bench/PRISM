Feature: PRISM-14
  Scenario: PRISM-14
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-14
    When Cancel the order the assistant is showing.
    Then A confirmation that the order was cancelled is shown.
