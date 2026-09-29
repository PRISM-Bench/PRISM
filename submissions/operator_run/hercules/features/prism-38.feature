Feature: PRISM-38
  Scenario: PRISM-38
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-38
    When Using only the keyboard, advance the signup to the next step.
    Then A confirmation that the step advanced is shown.
