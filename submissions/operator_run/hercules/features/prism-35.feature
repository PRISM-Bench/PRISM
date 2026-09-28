Feature: PRISM-35
  Scenario: PRISM-35
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-35
    When Publish the article.
    Then A confirmation that the article was published is shown.
