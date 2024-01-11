from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import re
from dataclasses import dataclass

from technologies_list import TECHNOLOGIES
from config import BASE_URL


chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get(BASE_URL)


@dataclass
class Vacancy:
    title: str
    description: str
    location: str
    experience: int
    english: str
    technologies: str


def get_years_from_experience(sentence: str) -> int | None:
    for char in sentence:
        if char.isdigit():
            return int(char)
    return None


def get_experience_from_additional_info(additional_info: list) -> tuple[int | None, str | None]:
    experience = None
    english = None
    pattern = r"(Fluent|Advanced|Upper-Intermediate|Intermediate|Beginner)"
    for categories in additional_info[1:]:
        if "досвід" in categories:
            experience = get_years_from_experience(categories)
        found_english = re.findall(pattern, categories)
        english = found_english[0] if found_english else None
    return experience, english


def get_technologies_from_description(description: str) -> str:
    pattern = re.compile(r'\b(?:' + '|'.join(TECHNOLOGIES) + r')\b', flags=re.IGNORECASE)
    found_technologies = set(re.findall(pattern, description))
    return ", ".join(found_technologies)


def parse_vacancy(temp_vacancy: driver) -> Vacancy:
    info = temp_vacancy.find_element(By.CLASS_NAME, "job-list-item__job-info").text.split("·")
    detail_description = temp_vacancy.find_element(By.CSS_SELECTOR, "div.job-list-item__description span").get_attribute("data-original-text").replace("<br>", " ") #TODO: find better way to get description
    description = temp_vacancy.find_element(By.CLASS_NAME, "job-list-item__description").text
    experience, english = get_experience_from_additional_info(info)
    technologies = get_technologies_from_description(detail_description)
    return Vacancy(
        title=temp_vacancy.find_element(By.CLASS_NAME, "job-list-item__link").text,
        description=description,
        location=temp_vacancy.find_element(By.CLASS_NAME, "location-text").text,
        experience=experience,
        english=english,
        technologies=technologies
    )


def parse_with_pagination() -> list | None:
    ex_list = []
    while True:
        for vacancy in driver.find_elements(By.CLASS_NAME, "job-list-item"):
            ex_list.append(parse_vacancy(vacancy))
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "ul.pagination_with_numbers li.page-item.active + li.page-item a.page-link")
            if "#" not in next_button.get_attribute("href"):
                next_button.click()
            else:
                return ex_list
        except NoSuchElementException:
            break
