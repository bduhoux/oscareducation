Feature: ClassCreation
  As a user
  I want to be able to create a class
  In order to manage my students online

  Scenario: Successfully creating a class
    Given The db is populated
    Given I am an existing non logged professor
    Then I log in
    Then I go on class creation page
    Then I create a class "foobar"
    Then I create two students, "Jean" "Khule" and "Bill" "Boquet" for my class
    Then I am on the class homepage
