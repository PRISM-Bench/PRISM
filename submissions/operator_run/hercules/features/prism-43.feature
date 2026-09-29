Feature: PRISM-43
  Scenario: PRISM-43
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-43
    When Fill in the card details below and place the order.
    And I use these values:
      | card_number  | 4242 4242 4242 4242 |
      | name_on_card | Ada Lovelace |
    Then A confirmation that the order was placed is shown.
