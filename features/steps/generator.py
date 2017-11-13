import re

from behave import given, when, then
from selenium.webdriver.support.select import Select


@given('I am on the generator page')
def step_impl(context):
    br = context.browser
    assert br.find_element_by_id("id_question_generator")


@then('I enter "{low}" as lower range and "{up}" as upper range')
def step_impl(context, low, up):
    br = context.browser
    br.find_element_by_id("id_range_from").send_keys(low)
    br.find_element_by_id("id_range_to").send_keys(up)


@when('I click on the create button')
def step_impl(context):
    br = context.browser
    br.find_element_by_id("id_generate_button").click()


@then('I see a list of generated problems')
def step_impl(context):
    br = context.browser
    assert br.find_element_by_id("id_generated_questions_page")


@then('I see an error panel')
def step_impl(context):
    br = context.browser
    assert br.find_element_by_id("id_error_panel")


@then('I click on generate the question')
def step_impl(context):
    br = context.browser
    br.find_element_by_id("id_generate_button").click()


@then('I choose a generated problem')
def step_impl(context):
    br = context.browser
    br.find_element_by_xpath("//button[@type='submit']").click()


@then('I click on going back to the test')
def step_impl(context):
    br = context.browser
    br.find_element_by_id("return-to-test-modify").click()


@then('I select the rational domain')
def step_impl(context):
    br = context.browser
    Select(br.find_element_by_id("id_domain")).select_by_value("Rational")

