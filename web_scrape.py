import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

URL = "https://cetcell.mahacet.org/"
print(f"Fetching announcements from: {URL}...\n")

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

try:
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(URL)
    
    print("Page loaded. Waiting 10 seconds for all content to appear...")
    time.sleep(10)
    
    print("Grabbing HTML source...")
    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')
    
    # --- THIS IS THE CORRECTED LINE ---
    announcement_list = soup.find('ul', class_='educms-download-marquee-content-items')
    # --------------------------------

    if announcement_list:
        # find_all('li') searches for all list items inside our target list
        announcements = announcement_list.find_all('li')
        
        print("\n----------- LATEST ANNOUNCEMENTS (SUCCESS!) -----------")
        for index, announcement in enumerate(announcements):
            # Find the link tag, if it exists
            link = announcement.find('a')
            if link:
                # .strip() removes extra whitespace
                print(f"{index + 1}. {link.text.strip()}")
        print("-----------------------------------------------------")
    else:
        print("\nScraping failed. The final class name did not work.")

except Exception as e:
    print(f"\nAn error occurred: {e}")