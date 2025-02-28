import time
import os
from selenium.webdriver.common.by import By
from selenium import webdriver

from WEB.VISUALIZATION import draw_box
from WEB.AI import LLM_CHAT


class WebScraper:
    def __init__(self, url, user_intent):
        self.url = url
        self.user_intent = user_intent
        self.driver = webdriver.Chrome()
        self.texts = set()
        self.chat = LLM_CHAT()

    def open_page(self):
        self.driver.get(self.url)

    def collect_elements(self):
        print(self.driver.current_url)
        self.texts = set()

        for element in self.driver.find_elements(By.XPATH, "//*"):
            if draw_box(element, self.driver):
                if not element.text:
                    continue
                if element.get_attribute("href"):
                    self.texts.add(element.get_attribute("href"))
                self.texts.add(
                    (
                        element.text,
                        (
                            element.get_attribute("href")
                            if element.get_attribute("href")
                            else None
                        ),
                    )
                )

    def build_prompt(self):
        with open("prompt.md", "r") as f:
            prompt = f.read()
        prompt += self.user_intent + "\n"

        data = ""

        for idx, text in enumerate(self.texts):
            clickable = text[1] is not None
            data += f"{idx}: {text[0]} - Clickable: {clickable}\n"

        return prompt, data

    def process_response(self, prompt, data):

        prompt += data

        print(prompt)
        res = self.chat.get_response(prompt)
        os.system("clear")

        try:
            idx = int(res)
        except ValueError:
            print(res)

            with open("output.txt", "w") as f:
                f.write(res)

            self.driver.quit()
            exit()

        self.click(idx)

    def click(self, idx):

        texts = list(self.texts)

        for element in self.driver.find_elements(By.XPATH, "//*"):
            if element.text == texts[idx][0]:
                element.click()
                break

    def loop(self):
        time.sleep(3)
        self.collect_elements()
        prompt, data = self.build_prompt()
        self.process_response(prompt, data)

        self.texts = set()

    def run(self):
        self.open_page()

        while True:
            self.loop()


if __name__ == "__main__":
    url = "https://quotes.toscrape.com/"
    user_intent = "Give me some love quotes"
    scraper = WebScraper(url, user_intent)
    scraper.run()
