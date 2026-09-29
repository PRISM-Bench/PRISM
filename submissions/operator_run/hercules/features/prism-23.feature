Feature: PRISM-23
  Scenario: PRISM-23
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-23
    When Drag the logo to the requested zone.
    Then A confirmation that the logo landed in the right zone is shown.
