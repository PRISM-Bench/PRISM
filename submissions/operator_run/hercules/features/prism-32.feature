Feature: PRISM-32
  Scenario: PRISM-32
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-32
    When Enter the profile details below, moving through each stage. Save the profile.
    And I use these values:
      | name     | Ada Lovelace |
      | email    | ada.lovelace@example.com |
      | phone    | +1 555 0142 |
      | location | London |
    Then The confirmation shows the name "Ada Lovelace".
