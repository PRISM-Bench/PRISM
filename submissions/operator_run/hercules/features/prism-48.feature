Feature: PRISM-48
  Scenario: PRISM-48
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-48
    When Look up the receipt for this order and note the confirmation code it shows. Enter that code on the checkout form and finish the purchase.
    Then A confirmation that the purchase went through is shown.
