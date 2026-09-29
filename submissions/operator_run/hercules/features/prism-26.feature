Feature: PRISM-26
  Scenario: PRISM-26
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-26
    When Update the profile name to the value below and save it.
    And I use these values:
      | name | Updated Name |
    Then The profile shows the updated name.
