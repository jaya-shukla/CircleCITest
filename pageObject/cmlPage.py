from playwright.sync_api import expect

from utils.helper import read_json_file
from utils.locators import *


class CMLLoginPage:
    inputData = read_json_file('data/inputData.json')

    def __init__(self, page):
        self.page = page


    def navigate(self):
        self.page.goto(self.inputData['gt3_url'])


    def accept_cookie_banner(self):
        try:
            accept_button = self.page.locator("#onetrust-accept-btn-handler")
            accept_button.wait_for(state="visible", timeout=5000)
            accept_button.click()
        except Exception:
            print("Cookie banner not found or already accepted")


    def login_user_cml(self,user_credentials):
        self.page.locator(USERNAME_INPUT).fill(user_credentials["userEmail"])
        self.page.get_by_role("button", name="Continue").click()
        self.page.fill(PASSWORD_INPUT, user_credentials["userPassword"])
        self.page.get_by_role(**CONTINUE_BUTTON).click()

    def click_ep_link(self):
        self.page.get_by_text(EMAIL_PROTECTION_TEXT).click()

    def click_account_selector(self):
        self.page.locator(ACCOUNT_SELECTOR).click()

    def select_account(self, account_name):
        self.page.locator(f'//*[@role="menuitem"]//span[text()="{account_name}"]').click()
        expect(self.page.locator(ACCOUNT_SELECTOR)).to_contain_text(account_name, timeout=200000)