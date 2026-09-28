Feature: PRISM-49
  Scenario: PRISM-49
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-49
    When Drag the ticket card from To Do to Done.
    Then A confirmation that the card reached Done is shown.
