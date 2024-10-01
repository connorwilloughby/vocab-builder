from pandas import read_html, concat

from selenium import webdriver
from selenium.webdriver.common.by import By


def scrape_1k():
    """
    Scrape and save a decent file from 1k words.
    """

    driver = webdriver.Chrome()
    driver.get(
        "https://1000mostcommonwords.com/1000-most-common-spanish-words/"
    )

    raw_tables = driver.find_elements(By.TAG_NAME, "table")

    cleaned_html = [table.get_attribute("outerHTML") for table in raw_tables]

    raw_concat = [read_html(raw_html) for raw_html in cleaned_html]

    final_frame = concat(raw_concat)

    return final_frame


if __name__ == "__main__":
    scrape_1k()
