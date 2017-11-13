# encoding: utf-8
from behave import given, when, then
from django.contrib.auth.hashers import make_password
from selenium.webdriver.support.select import Select
import re


@given('I am an existing non logged professor')
def step_impl(context):
    from test.factories.user import ProfessorFactory
    u = ProfessorFactory.create(user__username="username", user__password=make_password("password"))
    u.save()


@then('I log in')
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/accounts/usernamelogin/')
    assert br.current_url.endswith('/accounts/usernamelogin/')
    br.find_element_by_id("id_username").send_keys('username')
    br.find_element_by_xpath("//input[@type='submit']").click()
    assert br.current_url.endswith('/accounts/passwordlogin/')
    br.find_element_by_id("id_password").send_keys('password')
    br.find_element_by_xpath("//input[@type='submit']").click()
    assert br.current_url.endswith('/professor/dashboard/')


@then('I create the class "{classname}", with students "{firstname1}" "{lastname1}" and "{firstname2}" "{lastname2}"')
def step_impl(context, classname, firstname1, lastname1, firstname2, lastname2):
    br = context.browser
    br.find_element_by_id("id_add_lesson").click()
    assert br.current_url.endswith('professor/lesson/add/')
    br.find_element_by_id("id_name").send_keys(classname)
    Select(br.find_element_by_id("id_stage")).select_by_value("13")
    br.find_element_by_xpath("//button[@type='submit']").click()
    assert re.search(r'/professor/lesson/[0-9]+/student/add/', br.current_url)
    br.find_element_by_xpath("//input[@name='first_name_0']").send_keys(firstname1)
    br.find_element_by_xpath("//input[@name='last_name_0']").send_keys(lastname1)
    br.find_element_by_xpath("//input[@name='first_name_1']").send_keys(firstname2)
    br.find_element_by_xpath("//input[@name='last_name_1']").send_keys(lastname2)
    br.find_element_by_xpath("//button[@type='submit']").click()
    assert re.search(r'/professor/lesson/[0-9]+', br.current_url)


@then('I create the test "{test_name}" for skill "{skill}"')
def step_impl(context, test_name, skill):
    br = context.browser
    br.find_element_by_id("id_my_tests_button").click()
    assert re.search(r'/professor/lesson/[0-9]+/test/', br.current_url)
    br.find_element_by_id("id_add_test_button").click()
    assert re.search(r'/professor/lesson/[0-9]+/test/add', br.current_url)
    br.find_element_by_id("id_add_test_online_button").click()
    assert re.search(r'/professor/lesson/[0-9]+/test/online/add', br.current_url)
    Select(br.find_element_by_xpath("//select[@ng-model='stage13SelectedSkill']")).select_by_value(skill)
    # Adding the competence
    br.find_element_by_id("addSkillToTestButtonForStage13").click()
    br.find_element_by_id("addSkillToTestButtonForStage13").click()
    br.find_element_by_id("addSkillToTestButtonForStage13").click()
    # Add name to test
    br.find_element_by_id("test_name").send_keys(test_name)
    # Create the test
    br.find_element_by_id("id_create_test_button").click()


@given('The db is populated')
def step_impl(context):
    populate_stages_in_db()


def populate_stages_in_db():
    from test.factories.stage import StageFactory
    from test.factories.skill import SkillFactory
    from test.factories.skill import SectionFactory

    SectionFactory.create(id=28, name="UAA5: Deuxième degré").save()

    skilla = SkillFactory.create(id=342, code="T4-U5-A1b",
                        name="Résoudre algébriquement une équation ou une inéquation du 2e degré", description="",
                        image="area-chart", oscar_synthese=None, modified_by_id=None, section_id=28)

    skilla.save()

    StageFactory.create(id=1, name="étape I (1er degré primaire)", short_name="1e", level=1,
                        previous_stage_id=None).save()
    StageFactory.create(id=9, name="étape II (2e et 3e degrés primaire)", short_name="2e", level=2,
                        previous_stage_id=1).save()
    StageFactory.create(id=3, name="étape III (1er degré secondaire)", short_name="3e", level=3,
                        previous_stage_id=9).save()
    StageFactory.create(id=10, name="2e degré professionnel", short_name="2p", level=4,
                        previous_stage_id=3).save()
    StageFactory.create(id=11, name="3e degré professionnel", short_name="3p", level=5,
                        previous_stage_id=10).save()
    StageFactory.create(id=18, name="2e degré technique (2 pér./sem.)", short_name="2d2", level=4,
                        previous_stage_id=3).save()
    StageFactory.create(id=19, name="3e degré technique (2 pér./sem.)", short_name="3d2", level=5,
                        previous_stage_id=18).save()
    StageFactory.create(id=12, name="3e année transition", short_name="3t", level=4,
                        previous_stage_id=3).save()
    StageFactory.create(id=13, name="4e année transition", short_name="4t", level=5,
                        previous_stage_id=12, skills=(skilla,)).save()
    StageFactory.create(id=14, name="5e année transition (mathématiques de base)", short_name="5tb", level=6,
                        previous_stage_id=13).save()
    StageFactory.create(id=15, name="6e année transition (mathématiques de base)", short_name="6tb", level=7,
                        previous_stage_id=14).save()
    StageFactory.create(id=16, name="5e année transition (mathématiques générales)", short_name="5tg", level=6,
                        previous_stage_id=13).save()
    StageFactory.create(id=17, name="6e année transition (mathématiques générales)", short_name="6tg", level=7,
                        previous_stage_id=16).save()
