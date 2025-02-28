from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from WEB.AI import LLM_CHAT

llm = LLM_CHAT()

driver = webdriver.Chrome()
driver.get("https://quotes.toscrape.com/")

llm.get_response(
    "The user wants to go to the section with inspirational quotes... here is the page source, return the path of an "
    f"{driver.page_source}"
    "The user wants to go to the section with inspirational quotes... here is the page source, return the path of an "
)
