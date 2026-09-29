Feature: PRISM-09
  Scenario: PRISM-09
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-09
    When Confirm the booking.
    Then A confirmation that the booking was placed is shown.
