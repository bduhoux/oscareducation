from behave import given, when, then


@given('I am on the login page')
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/accounts/usernamelogin/')
    assert br.current_url.endswith('/accounts/usernamelogin/')


@then('I enter my username')
def step_impl(context):
    br = context.browser
    br.find_element_by_id("id_username").send_keys('username')


@when('I submit my username')
def step_impl(context):
    br = context.browser
    br.find_element_by_xpath("//input[@type='submit']").click()


@then('I am on the password page')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith('/accounts/passwordlogin/')


@then('I enter my password')
def step_impl(context):
    br = context.browser
    br.find_element_by_id("id_password").send_keys('password')


@when('I submit my password')
def step_impl(context):
    br = context.browser
    br.find_element_by_xpath("//input[@type='submit']").click()


@given('I am an existing non logged student')
def step_impl(context):
    from test.factories.user import StudentFactory
    u = StudentFactory.create()
    u.save()


@then('I am redirected to the professor home page')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith('/professor/dashboard/')


@then('I am redirected to the student home page')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith('/student/dashboard/')


@then('I enter an invalid username')
def step_impl(context):
    br = context.browser
    br.find_element_by_id("id_username").send_keys('WRONGUSERNAME')


@then('I enter an invalid password')
def step_impl(context):
    br = context.browser
    br.find_element_by_id("id_password").send_keys('WRONGPASSWORD')


# FIXME : This distinction should not even occur as it gives to much information about whether a username is valid
@then('I am redirected to the login fail page')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith('/accounts/passwordlogin/') or br.current_url.endswith('/accounts/usernamelogin/')
    assert br.find_element_by_class_name('alert-danger')