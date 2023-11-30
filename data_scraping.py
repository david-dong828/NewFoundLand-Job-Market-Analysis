# Name: Dong Han
# Student ID: 202111878
# Mail: dongh@mun.ca
import re

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.manifold import TSNE

############################################# COLLECT DATA #############################################
### Save 2 files: "xxx_jobs_partial.csv", "xxx_jobs_final_all.csv"
def scrape_jobpostwebsite_sel(start_index, increment, max_pages):
    # Base URL for the first page
    base_url = "https://ca.jobwebsite.com/jobs?q=&l=Newfoundland" #GONNA need a correct website

    # Set up Chrome options for Selenium
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # List to store job data
    all_jobs = []

    for page in range(max_pages):
        try:
            url = f"{base_url}&start={start_index + page * increment}"
            driver.get(url)

            wait = WebDriverWait(driver, 10)  # 10 seconds wait
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'slider_item')))  # Wait for job cards

            # Get the updated URL
            updated_url = driver.current_url

            # Print the updated URL
            print("Updated URL:", updated_url)

            # Update class names based on the HTML structure of the job listings
            job_cards = driver.find_elements(By.CLASS_NAME, 'slider_item')
            print(job_cards)
            for card in job_cards:
                title = card.find_element(By.CLASS_NAME, 'jobTitle').text
                company = card.find_element(By.CSS_SELECTOR, '[data-testid="company-name"]').text
                location = card.find_element(By.CSS_SELECTOR, '[data-testid="text-location"]').text
                salary_elements  = card.find_elements(By.CSS_SELECTOR, '[data-testid="attribute_snippet_testid"]')
                salary = salary_elements[0].text if salary_elements else 'N/A'
                job_type = card.find_elements(By.CSS_SELECTOR, '[data-testid="attribute_snippet_testid"]')[1].text if len(
                    card.find_elements(By.CSS_SELECTOR, '[data-testid="attribute_snippet_testid"]')) > 1 else 'N/A'
                description = ' '.join([li.text for li in card.find_elements(By.TAG_NAME, 'li')])
                date_posted = card.find_element(By.CLASS_NAME, 'date').text

                all_jobs.append({
                    'Title': title,
                    'Company': company,
                    'Location': location,
                    'Salary': salary,
                    'Job Type': job_type,
                    'Description': description,
                    'Date Posted': date_posted
                })

                # Save data to CSV after each page
                pd.DataFrame(all_jobs).to_csv('xxx_jobs_partial.csv', index=False)

        except Exception as e:
            print(f"Error on page {page}: {e}")
            break  # or continue, depending on

    # Close the browser
    driver.quit()
    print('Scraping complete.')

    # Save final consolidated data
    pd.DataFrame(all_jobs).to_csv('xxx_jobs_final_all.csv', index=False)




#############################################    MAIN    #############################################
def main():
    # Call to scrape data and save data to CSV
    # Scrape 50 pages at most incase banned by the website
    scrape_jobpostwebsite_sel(start_index=500, increment=10, max_pages=50)

if __name__ == '__main__':
    main()
