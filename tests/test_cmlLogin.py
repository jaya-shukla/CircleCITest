import pytest
from playwright.sync_api import Page, expect

from pageObject.cmlPage import CMLLoginPage
from utils.helper import *

from utils.helper import setup_logger, read_json_file
from utils.locators import *

filename = os.path.basename(__file__).replace(".py", ".log")
logger = setup_logger(__name__, log_file=filename)
user_credentials_list = read_json_file('data/credentials.json')['gt3_user_credentials']

@pytest.mark.parametrize("user_credentials", user_credentials_list)
def test_cml_login_ui(page: Page, user_credentials):
    login_page = CMLLoginPage(page)
    page.set_default_timeout(20000)
    logger.info("Navigating to CML login page")
    login_page.navigate()
    logger.info("Accepting cookie banner")
    login_page.accept_cookie_banner()
    logger.info("Checking EGD title in page title")
    assert EGD_TITLE in page.title()
    logger.info("Expecting sign-in page title")
    expect(page).to_have_title(SIGN_IN_TITLE,timeout=20000)
    logger.info(f"Logging in with user: {user_credentials['userEmail']}")
    login_page.login_user_cml(user_credentials)
    logger.info("Waiting for Email Protection text to be visible")
    expect(page.get_by_text(EMAIL_PROTECTION_TEXT)).to_be_visible(timeout=20000)
    logger.info("Clicking Email Protection link")
    login_page.click_ep_link()
    logger.info("Checking masthead titles for EP title")
    expect(page.locator(MASTHEAD_TITLES)).to_contain_text(EP_TITLE,timeout=20000)
    logger.info("Clicking account selector")
    login_page.click_account_selector()
    logger.info(f"Selecting account: {JAYA_BREW}")
    login_page.select_account(JAYA_BREW)
    logger.info("Checking selected account text")
    expect(page.locator(ACCOUNT_SELECTED)).to_contain_text(JAYA_BREW)
    logger.info("Checking visibility of first list item container")
    expect(page.locator(LIST_ITEM_CONTAINER).nth(0)).to_be_visible(timeout=20000)
    count = page.locator(LIST_ITEM_CONTAINER).count()
    assert count > 1, "Email list is not available on the page"
    logger.info(f"List item container count in page one: {count}")