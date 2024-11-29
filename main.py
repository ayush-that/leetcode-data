import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep


def setup_driver():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    return driver


def get_topics(url):
    """Scrape the topics from a LeetCode problem page."""
    leetcode_url = f"https://leetcode.com{url}"
    driver = setup_driver()
    driver.get(leetcode_url)
    sleep(2)  # Add a small delay to allow JavaScript to render

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Find Topics based on the div structure
    topics_div = soup.find("div", class_="mt-2 flex flex-wrap gap-1 pl-7")
    if topics_div:
        topics = [tag.text.strip() for tag in topics_div.find_all("a")]
        return ", ".join(topics) if topics else "No Topics Found"
    return "No Topics Found"


def process_file(file):
    """Process the CSV file to scrape topics."""
    df = pd.read_csv(file)
    if "Topics" not in df.columns:
        df["Topics"] = None

    for index, row in df.iterrows():
        if pd.isna(row["Topics"]):
            try:
                topics = get_topics(row["URL"])
                df.at[index, "Topics"] = topics
                print(f"Scraped Topics for {row['URL']}: {topics}")
            except Exception as e:
                print(f"Error scraping {row['URL']}: {e}")

    df.to_csv(file, index=False)
    print(f"Updated file saved: {file}")


def process_csv_files_parallel():
    """Process all CSV files in the current folder and update them with Topics."""
    current_folder = os.getcwd()
    files = [file for file in os.listdir(current_folder) if file.endswith(".csv")]

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_file, files)


if __name__ == "__main__":
    process_csv_files_parallel()
