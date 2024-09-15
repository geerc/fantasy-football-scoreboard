from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
driver = webdriver.Chrome(service=Service('/Users/christiangeer/Downloads/chromedriver-mac-x64/chromedriver'), options=options)

driver.get('https://sleeper.com/leagues/1048317772746416128/league')

content = driver.page_source
# Use BeautifulSoup or another library to parse the content
from bs4 import BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Extract the data you need
print(soup.prettify())

driver.quit()
