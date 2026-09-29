Feature: PRISM-10
  Scenario: PRISM-10
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-10
    When Acknowledge the report.
    Then A confirmation that the report was acknowledged is shown.
