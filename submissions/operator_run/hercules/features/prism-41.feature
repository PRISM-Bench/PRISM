Feature: PRISM-41
  Scenario: PRISM-41
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-41
    When Export the report.
    Then A confirmation that the export succeeded is shown.
