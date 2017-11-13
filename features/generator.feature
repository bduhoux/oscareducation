Feature: Generator
  As a user
  I want to be able to automatically creates questions
  In order to easily populates my assessments

  Scenario: Successfully creating an arithmetic problem
    Given The db is populated
    Given I am an existing non logged professor
    Then I log in
    Then I create the class "fuzzz", with students "Millui" "Cenlignes" and "Fatmodels" "Skinnycontrollers"
    Then I create the test "fizz" for skill "T4-U5-A1b"
    Then I click on generate the question
    Given I am on the generator page
    Then I enter "0" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an arithmetic problem with rational domain
    Given The db is populated
    Given I am an existing non logged professor
    Then I log in
    Then I create the class "fuzzz", with students "Millui" "Cenlignes" and "Fatmodels" "Skinnycontrollers"
    Then I create the test "fizz" for skill "T4-U5-A1b"
    Then I click on generate the question
    Given I am on the generator page
    Then I enter "0" as lower range and "60" as upper range
    Then I select the rational domain
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test


  Scenario: Trying to create an arithmetic problem without parameters
    Given The db is populated
    Given I am an existing non logged professor
    Then I log in
    Then I create the class "fuzzz", with students "Millui" "Cenlignes" and "Fatmodels" "Skinnycontrollers"
    Then I create the test "fizz" for skill "T4-U5-A1b"
    Then I click on generate the question
    Given I am on the generator page
    When I click on the create button
    Then I see an error panel

  Scenario: Trying to create an arithmetic problem with invalid range
    Given The db is populated
    Given I am an existing non logged professor
    Then I log in
    Then I create the class "fuzzz", with students "Millui" "Cenlignes" and "Fatmodels" "Skinnycontrollers"
    Then I create the test "fizz" for skill "T4-U5-A1b"
    Then I click on generate the question
    Given I am on the generator page
    Then I enter "99999" as lower range and "-1" as upper range
    When I click on the create button
    Then I see an error panel

  Scenario: Trying to create an arithmetic problem with too small range
    Given The db is populated
    Given I am an existing non logged professor
    Then I log in
    Then I create the class "fuzzz", with students "Millui" "Cenlignes" and "Fatmodels" "Skinnycontrollers"
    Then I create the test "fizz" for skill "T4-U5-A1b"
    Then I click on generate the question
    Given I am on the generator page
    Then I enter "0" as lower range and "1" as upper range
    When I click on the create button
    Then I see an error panel