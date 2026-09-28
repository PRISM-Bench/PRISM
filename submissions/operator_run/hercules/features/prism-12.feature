Feature: PRISM-12
  Scenario: PRISM-12
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-12
    When Enter the requested date in each of the three date fields. Save the schedule.
    Then A confirmation that the schedule was saved is shown.
