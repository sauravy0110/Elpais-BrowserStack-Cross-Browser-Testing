import click
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import requests
import http.client
import json
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options as ChromeOptions
from elpais_core import run_assignment

load_dotenv()



USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

BS_URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"



CAPABILITIES = [

    {
        "browserName": "Firefox",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "projectName": "Elpais Cross Browser Testing",
            "buildName": "Elpais Cross Browser Testing",
            "sessionName": "El Pais - Firefox Windows 10",
        },
    },

    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "projectName": "Elpais Cross Browser Testing",
            "buildName": "Elpais Cross Browser Testing",
            "sessionName": "El Pais - Chrome Windows 10",
        },
    },

    {
        "bstack:options": {
            "deviceName": "iPhone 17 Pro",
            "osVersion": "26",
            "realMobile": "true",
            "projectName": "Elpais Cross Browser Testing",
            "buildName": "Elpais Cross Browser Testing",
            "sessionName": "El Pais - iPhone 17 Pro",
        },
    },

    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "projectName": "Elpais Cross Browser Testing",
            "buildName": "Elpais Cross Browser Testing",
            "sessionName": "El Pais - Chrome Windows 11",
        },
    },

    {
        "browserName": "chromium",
        "bstack:options": {
            "deviceName": "iPhone 15 Pro Max",
            "osVersion": "17",
            "realMobile": "true",
            "projectName": "Elpais Cross Browser Testing",
            "buildName": "Elpais Cross Browser Testing",
            "sessionName": "El Pais - iPhone 15 Pro Max",
        },
    },

]

def run_on_capability(capability):

    driver = None
    name = capability["bstack:options"]["sessionName"]

    try:

        options = ChromeOptions()

        for key, value in capability.items():

            options.set_capability(
                key,
                value
            )

        driver = webdriver.Remote(
            command_executor=BS_URL,
            options=options
        )

        print(f"\n=== Starting session: {name} ===")

        run_assignment(driver, name)


        # Mark session as PASSED on BrowserStack

        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", '
            '"arguments": {"status": "passed", '
            '"reason": "El Pais automation completed successfully"}}'
        )


        print(f"=== Finished session: {name} ===")

        return name, None


    except Exception as e:

        print(f"\n[FAILED] {name}")

        print("Message:", e)


        # Mark session as FAILED on BrowserStack

        if driver:

            try:

                driver.execute_script(
                    'browserstack_executor: {"action": "setSessionStatus", '
                    '"arguments": {"status": "failed", '
                    '"reason": "Automation test failed"}}'
                )

            except Exception:

                pass


        traceback.print_exc()

        return name, e


    finally:

        if driver:

            driver.quit()


def main():

    if not USERNAME or not ACCESS_KEY:

        raise RuntimeError(
            "Set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY in .env file"
        )


    with ThreadPoolExecutor(max_workers=5) as executor:

        futures = {}


        for capability in CAPABILITIES:

            future = executor.submit(
                run_on_capability,
                capability
            )

            futures[future] = capability["bstack:options"]["sessionName"]


        for future in as_completed(futures):

            name = futures[future]

            session_name, error = future.result()


            if error:

                print("\n[FAILED] " + session_name)

                print(error)


            else:

                print("\n[SUCCESS] " + session_name)


if __name__ == "__main__":

    main()