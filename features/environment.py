from datetime import datetime
from selenium import webdriver
import django
from django.test.runner import DiscoverRunner
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.shortcuts import resolve_url
import os
import codecs
os.environ['DJANGO_SETTINGS_MODULE'] = 'oscar.settings'


def before_all(context):
    django.setup()
    context.test_runner = DiscoverRunner()
    context.old_db_config = context.test_runner.setup_databases()
    # PhantomJS is used there (headless browser - meaning we can execute tests in a command-line environment,
    # which is what we want for use with SemaphoreCI
    # For debugging purposes, you can use the Firefox driver instead.
    context.browser = webdriver.PhantomJS()
    # Small unit of wait between instructions, allowing things to load
    context.browser.implicitly_wait(10)
    # Screen size must be wide enough to let PhantomJS find elements
    context.browser.set_window_size(1920, 1080)
    # Using a different port, not conflicting if server is booted up
    context.server_url = 'http://localhost:8080'


class BehaviorDrivenTestCase(StaticLiveServerTestCase):
    """
    Test case attached to the context during behave execution

    This test case prevents the regular tests from running.
    """

    def runTest(*args, **kwargs):
        pass


def before_scenario(context, _):
    context.test = BehaviorDrivenTestCase()
    context.test.setUpClass()
    context.test() # this starts a transaction

    context.base_url = context.test.live_server_url

    def get_url(to=None, *args, **kwargs):
        return context.base_url + (
            resolve_url(to, *args, **kwargs) if to else '')
    context.get_url = get_url


def after_scenario(context, _):
    pass


def after_all(context):
    # Explicitly quits the browser, otherwise it won't once tests are done
    context.browser.quit()
    context.test_runner.teardown_databases(context.old_db_config)


def before_feature(context, feature):
    # Code to be executed each time a feature is going to be tested
    pass


# After a single step
def after_step(context, step):
    if step.status == 'failed':
        # Screenshots where that step failed
        context.browser.save_screenshot('features/failures/screenshots/'
                                        + str(datetime.now()) + '-' + step.name + '.png')
        save_path = 'features/failures/pages'
        file_name = str(datetime.now()) + '-' + str(step.name) + '.html'
        complete_name = os.path.join(save_path, file_name)
        file_object = codecs.open(complete_name, "w", "utf-8")
        html = context.browser.page_source
        file_object.write(html)
