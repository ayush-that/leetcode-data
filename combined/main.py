import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_topics(url, use_selenium=False):
    """Scrape the topics from a LeetCode problem page."""
    leetcode_url = f"https://leetcode.com{url}"

    if use_selenium:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(leetcode_url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
    else:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(leetcode_url, headers=headers)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")

    topics_div = soup.find("div", class_="mt-2 flex flex-wrap gap-1 pl-7")
    if topics_div:
        topics = [tag.text.strip() for tag in topics_div.find_all("a")]
        return ", ".join(topics) if topics else "No Topics Found"
    return "No Topics Found"


def process_csv_files_in_current_folder(use_selenium=False):
    """Process all CSV files in the current folder and update them with Topics."""
    current_folder = os.getcwd()
    for file in os.listdir(current_folder):
        if file.endswith(".csv"):
            file_path = os.path.join(current_folder, file)
            print(f"Processing file: {file_path}")

            df = pd.read_csv(file_path)

            if "Topics" not in df.columns:
                df["Topics"] = None

            for index, row in df.iterrows():
                if pd.isna(row["Topics"]):
                    try:
                        topics = get_topics(row["URL"], use_selenium)
                        df.at[index, "Topics"] = topics
                        print(f"Scraped Topics for {row['URL']}: {topics}")
                    except Exception as e:
                        print(f"Error scraping {row['URL']}: {e}")

            df.to_csv(file_path, index=False)
            print(f"Updated file saved: {file_path}")


if __name__ == "__main__":
    use_selenium = input("Use Selenium? (yes/no): ").lower() == "yes"
    process_csv_files_in_current_folder(use_selenium)
