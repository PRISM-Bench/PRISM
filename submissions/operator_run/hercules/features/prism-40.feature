Feature: PRISM-40
  Scenario: PRISM-40
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-40
    When Resume the session, confirming the prompt that appears.
    Then A confirmation that the session was resumed is shown.
