from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_chrome_driver() -> webdriver.Chrome:
    """
    Create a chrome driver.
    Install an executable if the driver fails to be created.
    """

    chrome_options = Options()

    # Chromium command line switches:
    # https://peter.sh/experiments/chromium-command-line-switches/#log-level
    chrome_options.add_argument("--window-size=1440,900")
    # Only show error and fatal message.
    chrome_options.add_argument("--log-level=2")
    chrome_options.add_argument("--headless")

    try:
        driver = webdriver.Chrome(options=chrome_options)
    except SessionNotCreatedException:
        executable_path = ChromeDriverManager().install()
        driver = webdriver.Chrome(
            executable_path=executable_path, options=chrome_options
        )
    return driver
