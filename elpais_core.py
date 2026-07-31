from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import requests
import http.client
import json

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
def run_assignment(driver, name):

    driver.get('https://elpais.com/')

    try:
        driver.maximize_window()
    except:
        pass

    wait = WebDriverWait(driver, 10)

    try:

        popup = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "didomi-notice-agree-button")
            )
        )

        popup.click()

    except TimeoutException:

        try:

            mobile_popup = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[@class='pmConsentWall-button' and normalize-space()='Accept and continue']"
                    )
                )
            )

            mobile_popup.click()

        except TimeoutException:
            pass

    time.sleep(3)

    try:

        opinion = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//a[@cmp-ltrk='portada_menu'][normalize-space()='Opinión']"
                )
            )
        )

        opinion.click()

    except TimeoutException:

        menu = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "btn_open_hamburger")
            )
        )

        menu.click()

        opinion = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//a[@cmp-ltrk='header_hamburguesa' and normalize-space()='Opinión']"
                )
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView();",
            opinion
        )

        time.sleep(1)

        opinion.click()

    wait.until(
        EC.url_contains("/opinion/")
    )

    try:

        wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//article//h2//a")
            )
        )

    except TimeoutException:

        print(
            "BLOCKED: Prisa Media Site verification prevented article loading"
        )

        raise

    article_links = driver.execute_script(
        """
        return Array.from(
            document.querySelectorAll('article h2 a')
        ).slice(0, 5).map(
            article => article.href
        );
        """
    )

    translated_titles = []
    count = 1

    folder_name = name.replace(" ", "_")

    image_folder = os.path.join(
        "images",
        folder_name
    )

    os.makedirs(
        image_folder,
        exist_ok=True
    )

    # Visiting each article
    for link in article_links:

        driver.get(link)
        time.sleep(3)


        # Get Spanish Title
        title = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1")
            )
        ).text

        # Get Spanish Content
        paragraphs = driver.find_elements(By.XPATH, "//article//p")

        content = ""

        if len(paragraphs) > 0:

            for paragraph in paragraphs:
                content = content + paragraph.text + "\n"

        else:

            spans = driver.find_elements(
                By.XPATH,
                "//article//figcaption//span[not(contains(@class,'a_m_m'))]"
            )

            for span in spans:
                content = content + span.text + "\n"


        # Print Spanish Title and Content
        print("TITLE:")
        print(title)

        print("CONTENT:")
        print(content)

        # Download Cover Image
        images = driver.find_elements(
            By.XPATH,
            "//article//img[@loading='eager']"
        )

        if len(images) > 0:

            image_url = images[0].get_attribute("src")

            if image_url:

                response = requests.get(image_url)

                if response.status_code == 200:
                    file = open(
                        image_folder + "/article_" + str(count) + ".jpg",
                        "wb"
                    )

                    file.write(response.content)
                    file.close()

        # Translate Title
        conn = http.client.HTTPSConnection(
            "google-translate113.p.rapidapi.com"
        )

        payload = json.dumps({
            "from": "es",
            "to": "en",
            "json": {
                "title": title
            }
        })

        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "google-translate113.p.rapidapi.com",
            'Content-Type': "application/json"
        }

        conn.request(
            "POST",
            "/api/v1/translator/json",
            payload,
            headers
        )

        res = conn.getresponse()
        data = res.read()

        result = json.loads(data.decode("utf-8"))


        # Get and Print Translated Title
        if "trans" in result:

            translated_title = result["trans"]["title"]

            translated_titles.append(translated_title)

            print("TRANSLATED TITLE:")
            print(translated_title)

        else:

            print("TRANSLATION FAILED:")
            print(result)


        print("--------------------------------")

        count = count + 1


    # Analyze All Translated Titles

    all_words = []

    for title in translated_titles:

        words = title.lower().split()

        for word in words:
            all_words.append(word)


    word_count = {}

    for word in all_words:

        if word in word_count:
            word_count[word] = word_count[word] + 1

        else:
            word_count[word] = 1


    # Print Words Repeated More Than Twice

    print("WORDS REPEATED MORE THAN TWICE:")

    found = False

    for word in word_count:

        if word_count[word] > 2:

            print(word, "-", word_count[word])

            found = True


    if found == False:
        print(0)