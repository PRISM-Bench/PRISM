Feature: PRISM-04
  Scenario: PRISM-04
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-04
    When Enter the email address below and confirm it.
    And I use these values:
      | email | tester@example.com |
    Then A confirmation that the submission succeeded is shown.
