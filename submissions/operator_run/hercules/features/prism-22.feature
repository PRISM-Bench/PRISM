Feature: PRISM-22
  Scenario: PRISM-22
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-22
    When Pick a seat for the event and confirm it.
    Then A confirmation that the seat was reserved is shown.
