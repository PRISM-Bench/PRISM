Feature: PRISM-27
  Scenario: PRISM-27
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-27
    When Like the post.
    Then The post is shown as liked.
