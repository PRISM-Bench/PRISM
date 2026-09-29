Feature: PRISM-36
  Scenario: PRISM-36
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-36
    When Add two of the product to the cart.
    Then A confirmation that both items were added to the cart is shown.
