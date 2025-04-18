
#THIS CODE IS TO GET THE MAIN CATEGORY LINKS FROM AMAZON HOMEPAGE

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time
from random import randint
import os

options = Options()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


driver.get("https://www.amazon.in")

menu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "nav-xshop")))

category_links = menu.find_elements(By.CSS_SELECTOR, "a")
m = "minitv"
b = "/b/3"
g = "/gp/"
links = set()

for cl in category_links:
	link = cl.get_attribute("href")
	if m not in link and b not in link and g not in link:
		links.add(link)
		print(link)
		fp = os.open("main_cat_links", os.O_CREAT | os.O_RDWR | os.O_APPEND)
		os.write(fp,str.encode(link))
		os.write(fp,str.encode('\n'))
		os.close(fp)
		print()

time.sleep(randint(1,3))

driver.quit()


