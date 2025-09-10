Feature: Hit Counter
    As a website visitor
    I want to be able to click a button to make the counter go up
    So that I can see how many times I have clicked the button

Scenario 1: The counter goes up when the button is clicked
    Given the counter is reset
    When a user clicks the "Hit" button
    Then the counter should be at 1
    When a user clicks the "Hit" button
    Then the counter should be at 2