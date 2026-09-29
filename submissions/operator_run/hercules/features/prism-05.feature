Feature: PRISM-05
  Scenario: PRISM-05
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-05
    When Pay for the order using the details below.
    And I use these values:
      | card_number | 4242 4242 4242 4242 |
    Then A confirmation that the payment succeeded is shown.
