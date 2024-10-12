from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Initialize the Selenium WebDriver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no browser UI)
    driver = webdriver.Chrome(options=options)
    return driver

# Scrape job listings from Indeed
def scrape_jobs_indeed(driver, job_title, location):
    url = f"https://www.indeed.com/jobs?q={job_title}&l={location}"
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    jobs = []

    for job_card in soup.find_all('div', class_='jobsearch-SerpJobCard'):
        title = job_card.find('a', class_='jobtitle').text.strip()
        company = job_card.find('span', class_='company').text.strip()
        link = 'https://www.indeed.com' + job_card.find('a', class_='jobtitle')['href']
        jobs.append({'title': title, 'company': company, 'link': link})

    return jobs

# Scrape job listings from LinkedIn (not fully implemented)
def scrape_jobs_linkedin(driver, job_title, location):
    # This can be implemented similarly to Indeed scraping
    return []

