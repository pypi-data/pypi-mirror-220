import requests
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from liveramp_automation.util_log import Logger
from liveramp_automation.util_time import fixed_wait


class LoginHepler:

    # This method liveramp_okta_login_page is to login okta with Playwright.
    # The username and passowrd are requried.
    # Please try to call this API with the username and password provided in os.environ[]
    @staticmethod
    def liveramp_okta_login_page(page, config, username, password):
        # navigate to the Okta login page
        Logger.info("We are going to login to OKTA")
        url = config['login_url']
        Logger.info("The login url is {}".format(url))
        page.goto(url)
        fixed_wait()
        url_new = page.url
        Logger.info("The current url is {}".format(url_new))
        if url_new.__contains__(url):
            Logger.info("We've already logan to OKTA succefully")
        else:
            page.fill('#idp-discovery-username', username)
            page.get_by_role("button", name="Next").click()
            page.get_by_role("textbox", name="Password").fill(password)
            page.get_by_role("button", name="Sign In").click()
            Logger.info("We could login to OKTA successfully")
            # wait for the login process to complete
            fixed_wait(20)

    # This method liveramp_okta_login_driver is to login okta with Selenium.
    # The username and passowrd are requried.
    # Please try to call this API with the username and password provided in os.environ[]
    @staticmethod
    def liveramp_okta_login_driver(driver, config, username, password):
        # navigate to the Okta login page
        Logger.info("We are going to login to OKTA")
        url = config['login_url']
        Logger.info("The login url is {}".format(url))
        driver.get(url)
        fixed_wait()
        if driver.current_url.__contains__(url):
            Logger.info("We've already logan to OKTA succefully")
        else:
            username = driver.find_element(by=By.ID, value='idp-discovery-username')
            username.send_keys(username)
            username.send_keys(Keys.ENTER)
            fixed_wait()
            password = driver.find_element(by=By.ID, value='okta-signin-password')
            password.send_keys(password)
            submit_button = driver.find_element(by=By.ID, value='okta-signin-submit')
            submit_button.click()
            Logger.info("We could login to OKTA successfully")
            # wait for the login process to complete
            fixed_wait(20)

    # This method call_oauth2_get_token is to all oauth2 to login, the API username and password(sereect) are required.
    # The username and passowrd are requried.
    # Please try to call this API with the username and password provided in os.environ[]
    @staticmethod
    def call_oauth2_get_token(username, password):
        params = {
            "grant_type": "password",
            "scope": "openid",
            "client_id": "liveramp-api"
        }
        Logger.info("The default params are the {}".format(params))
        headers = {"content-type": "application/x-www-form-urlencoded"}
        params.update(username=username)
        params.update(password=password)
        response = requests.post(
            "https://serviceaccounts.liveramp.com/authn/v1/oauth2/token", params=params, headers=headers)
        assert 200 == response.status_code
        access_token = response.json()['access_token']
        return "Bearer {}".format(access_token)
