Feature: Manage Web Tables on DemoQA
  As a tester
  I want to create, edit and delete web table records
  So that I can verify the functionality works correctly

  @webtables
  Scenario: Create and delete multiple dynamic records
    Given I am on the Web Tables page
    When I create 12 dynamic records
    Then I delete all dynamic records
