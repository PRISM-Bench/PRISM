Feature: PRISM-29
  Scenario: PRISM-29
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-29
    When Set the appointment to the time slot the page names, then confirm it.
    Then A confirmation that the appointment was rescheduled is shown.
