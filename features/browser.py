"""
Browser configuration for the Behaviour-Driven-Development environment
"""
from selenium import webdriver
from datetime import datetime


class Browser(object):
    base_url = 'http://localhost:8080'
    driver = webdriver.PhantomJS()
    driver.implicitly_wait(60)
    driver.set_window_size(1920, 1080)

    def close(self):
        """
        close the webdriver instance
        """
        self.driver.quit()

    def visit(self, location):
        """
        navigate webdriver to different pages
        """
        self.driver.get(location)

    def find_element_by_id(self, selector):
        """
        find a page element in the DOM
        """
        return self.driver.find_element_by_id(selector)

    def find_element_by_type(self, selector):
        """
        find a page element in the DOM from the type
        """
        return self.driver.find_element_by_xpath("//input[@type='" + selector + "']")

    def find_element_by_datatesting(self, selector):
        """
        find a page element in the DOM based on a "data-testing" tag
        :param selector: string value of the data-testing tag
        :return: DOM element found
        """
        return self.driver.find_element_by_xpath("//input[@data-testing='" + selector + "']")

    def save_screenshot(self):
        return self.driver.save_screenshot('features/screenshots/' + str(datetime.now()) + '.png')