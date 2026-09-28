Feature: PRISM-03
  Scenario: PRISM-03
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-03
    When Confirm the booking.
    Then A confirmation that the booking succeeded is shown.
