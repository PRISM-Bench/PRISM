Feature: PRISM-39
  Scenario: PRISM-39
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-39
    When Send a message through the contact form.
    Then A confirmation that the message was sent is shown.
