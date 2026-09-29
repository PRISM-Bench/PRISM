Feature: PRISM-18
  Scenario: PRISM-18
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-18
    When Open the Privacy Policy from the bottom of the page.
    Then A confirmation that the privacy policy was opened is shown.
