Feature: PRISM-31
  Scenario: PRISM-31
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-31
    When Review the cart and check out.
    Then A confirmation that the checkout succeeded is shown.
