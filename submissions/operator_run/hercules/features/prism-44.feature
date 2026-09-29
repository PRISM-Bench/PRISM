Feature: PRISM-44
  Scenario: PRISM-44
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-44
    When View the report.
    Then A confirmation that the report was generated is shown.
