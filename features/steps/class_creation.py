import re

from behave import given, when, then
from selenium.webdriver.support.select import Select


@then('I go on class creation page')
def step_impl(context):
    br = context.browser
    br.find_element_by_id("id_add_lesson").click()
    assert br.current_url.endswith('professor/lesson/add/')


@then('I create a class "{classname}"')
def step_impl(context, classname):
    br = context.browser
    br.find_element_by_id("id_name").send_keys(classname)
    Select(br.find_element_by_id("id_stage")).select_by_value("13")
    br.find_element_by_xpath("//button[@type='submit']").click()
    assert re.search(r'/professor/lesson/[0-9]+/student/add/', br.current_url)


@then('I create two students, "{firstname1}" "{lastname1}" and "{firstname2}" "{lastname2}" for my class')
def step_impl(context, firstname1, lastname1, firstname2, lastname2):
    br = context.browser
    br.find_element_by_xpath("//input[@name='first_name_0']").send_keys(firstname1)
    br.find_element_by_xpath("//input[@name='last_name_0']").send_keys(lastname1)
    br.find_element_by_xpath("//input[@name='first_name_1']").send_keys(firstname2)
    br.find_element_by_xpath("//input[@name='last_name_1']").send_keys(lastname2)
    br.find_element_by_xpath("//button[@type='submit']").click()
    assert re.search(r'/professor/lesson/[0-9]+', br.current_url)


@then('I am on the class homepage')
def step_impl(context):
    br = context.browser
    assert re.search(r'/professor/lesson/[0-9]+', br.current_url)