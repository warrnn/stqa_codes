from behave import given, when, then
import requests

@given("the counter is reset")
def step_impl(context):
    # Send a post request to the appropriate route to reset
    response = requests.post(f"{context.base_url}/reset")
    # Assert the status code is 200
    assert response.status_code == 200
    
@when("a user clicks the 'Hit' button")
def step_impl(context):
    # Send a post request to the appropriate route to hit
    response = requests.post(f"{context.base_url}/hit")
    # Assert the status code is 200
    assert response.status_code == 200
    
@then("the counter should be at {count}")
def step_impl(context, count):
    # Send a get request to acquire the returned web page
    response = requests.get(f"{context.base_url}/")
    # Assert the counter has the expected value
    assert f"<span id=\"counter\">{count}</span>" in response.text