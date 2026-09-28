Feature: PRISM-08
  Scenario: PRISM-08
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-08
    When Fill in the details below and create the account.
    And I use these values:
      | full_name | Ada Lovelace |
      | email     | ada.lovelace@example.com |
      | password  | Prism-08-trial |
    Then A confirmation that the account was created is shown.
