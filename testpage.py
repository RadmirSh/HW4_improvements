import requests
import yaml
from BaseApp import BasePage
from selenium.webdriver.common.by import By
import logging

with open('testdata.yaml') as f:
    test_data = yaml.safe_load(f)
    browser = test_data['browser']

class TestSearchLocators:
    ids = dict()
    with open("./locators.yaml") as f:
        locators = yaml.safe_load(f)
    for locator in locators['xpath'].keys():
        ids[locator] = (By.XPATH, locators['xpath'][locator])
    for locator in locators['css'].keys():
        ids[locator] = (By.CSS_SELECTOR, locators['css'][locator])

class OperationsHelper(BasePage):

    def enter_text_into_field(self, locator, word, description=None):
        if description:
            element_name = description
        else:
            element_name = locator
        logging.debug(f'Send {word} to element {element_name}')
        field = self.find_element(locator)
        if not field:
            logging.error(f'Element {locator} not found')
            return False
        try:
            field.clear()
            field.send_keys(word)
        except:
            logging.exception(f'Exception while operation with {locator}')
            return False
        return True

    def click_button(self, locator, description=None):
        if description:
            element_name = description
        else:
            element_name = locator
        button = self.find_element(locator)
        if not button:
            return False
        try:
            button.click()
        except:
            logging.exception('Exception with click')
            return False
        logging.debug(f'Clicked {element_name} buttton')
        return True

    def get_text_from_element(self, locator, description=None):
        if description:
            element_name = description
        else:
            element_name = locator
        field = self.find_element(locator, time=3)
        if not field:
            return None
        try:
            text = field.text
        except:
            logging.exception(f'Exception while get test from {element_name}')
            return None
        logging.debug(f'We find text {text} in field {element_name}')
        return text

    # ENTER TEXT
    def enter_login(self, word):
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_LOGIN_FIELD'], word,
                                   description='login form')

    def enter_pass(self, word):
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_PASS_FIELD'], word,
                                   description='password form')

    def create_post_title(self, word):
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_CREATE_TITLE'], word,
                                   description='create post title form')

    def create_post_description(self, word):
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_CREATE_DESCRIPTION'], word,
                                   description='create post description form')

    def create_post_content(self, word):
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_CREATE_CONTENT'], word,
                                   description='create post content form')

    def contact_us_name(self, word):
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_YOUR_NAME'], word,
                                   description='create your name form')

    def contact_us_email(self, word):
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_YOUR_EMAIL'], word,
                                   description='create your mail form')

    def contact_us_content(self, word):
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_YOUR_CONTENT'], word,
                                   description='create your content form')

    def click_login_button(self):
        self.click_button(TestSearchLocators.ids['LOCATOR_LOGIN_BTN'], description= 'Login button')

    def click_create_button(self):
        self.click_button(TestSearchLocators.ids['LOCATOR_CREATE_BUTTON'], description='Create button')

    def click_create_post_button(self):
        self.click_button(TestSearchLocators.ids['LOCATOR_CREATE_POST_BTN'], description='Create post button')

    def click_contact(self):
        self.click_button(TestSearchLocators.ids['LOCATOR_CONTACT'], description='contact button')

    def click_contact_us(self):
        self.click_button(TestSearchLocators.ids['LOCATOR_CONTACT_US_BTN'], description='contact us button')

    def get_error_text(self):
        return self.get_text_from_element(TestSearchLocators.ids['LOCATOR_ERROR_FIELD'], description='error 401')

    def get_login_enter_text(self):
        return self.get_text_from_element(TestSearchLocators.ids['LOCATOR_LOGIN_ENTER'], description='login error')

    def get_res_create_text(self):
        return self.get_text_from_element(TestSearchLocators.ids['LOCATOR_RES_CREATE'], description='error create')

    def alert(self):
        alert = self.driver.switch_to.alert
        return alert.text

def login():
    try:
        response = requests.post(test_data['url_login'],
                                 data={'username': test_data['login_1'], 'password': test_data['password_1']})
        if response.status_code == 200:
            return response.json()['token']
        else:
            logging.error(f"Error login. Status code: {response.status_code}")
            return None
    except:
        logging.exception(f"Exception with login")
        return None

def get(token):
    try:
        resourсe = requests.get(test_data['url_posts'],
                            headers={'X-Auth-Token': token},
                            params={'owner': 'notMe'})
        if resourсe.status_code == 200:
            return resourсe.json()
        else:
            logging.error(f"Error with retrieving data. Status code: {resourсe.status_code}")
            return None
    except:
        logging.exception(f"Exception with get")
        return None

def post(token):
    try:
        new_post = requests.post(test_data['url_posts'],
                                data={'title': "Writer",
                                'description': "Pushkin",
                                'content':"A.S.Pushkin"},
                                headers={'X-Auth-Token': token})
        if new_post.status_code == 200:
            return new_post.json()
        else:
            logging.error(f"Error with posting data. Status code: {new_post.status_code}")
            return None
    except:
        logging.exception(f"Exception with post")
        return None

def get_post(token):
    try:
        resourсe = requests.get(test_data['url_posts'],
                            headers={'X-Auth-Token': token})
        if resourсe.status_code == 200:
            return resourсe.json()
        else:
            logging.error(f"Error with retrieving data. Status code: {resourсe.status_code}")
            return None
    except:
        logging.exception(f"Exception with get_post")
        return None