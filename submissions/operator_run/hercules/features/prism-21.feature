Feature: PRISM-21
  Scenario: PRISM-21
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-21
    When Select the highest point on the chart.
    Then A confirmation that the selection succeeded is shown.
