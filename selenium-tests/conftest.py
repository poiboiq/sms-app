import os
import time
import requests
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


BASE_URL = os.environ.get("BASE_URL", "http://web")
SELENIUM_REMOTE_URL = os.environ.get("SELENIUM_REMOTE_URL", "http://chrome:4444/wd/hub")


def wait_for_url(url: str, timeout: int = 90) -> None:
    last_error = None
    for _ in range(timeout):
        try:
            response = requests.get(url, timeout=3)
            if response.status_code < 500:
                return
        except Exception as exc:
            last_error = exc
        time.sleep(1)
    raise RuntimeError(f"Timed out waiting for {url}. Last error: {last_error}")


def wait_for_selenium(timeout: int = 90) -> None:
    status_url = SELENIUM_REMOTE_URL.replace("/wd/hub", "") + "/status"
    last_error = None
    for _ in range(timeout):
        try:
            response = requests.get(status_url, timeout=3)
            if response.ok:
                return
        except Exception as exc:
            last_error = exc
        time.sleep(1)
    raise RuntimeError(f"Timed out waiting for Selenium at {status_url}. Last error: {last_error}")


@pytest.fixture(scope="session")
def base_url():
    wait_for_selenium()
    wait_for_url(BASE_URL)
    return BASE_URL


@pytest.fixture
def driver(base_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1440,1000")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    browser = webdriver.Remote(
        command_executor=SELENIUM_REMOTE_URL,
        options=chrome_options,
    )
    browser.implicitly_wait(2)
    yield browser
    browser.quit()
