Feature: PRISM-47
  Scenario: PRISM-47
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-47
    When Make a small edit to the draft. Undo that edit. Save the draft and confirm.
    Then A confirmation that the draft was saved is shown.
