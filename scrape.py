#THIS CODE HAS THREE PARTS TO IT:
# 1. SCRAPING SUBCATEGORY LINKS FROM THE MAIN CATEGORY LINKS THAT WE HAVE GOT FROM THE AMAZON HOMEPAGE (IN CODE main_links.py) AND WRITING
#	 THEM IN A FILE SUB_CAT_LINKS(scrape_sub_cat_links)
# 2. SCRAPING PRODUCT LINKS FROM THE SUBCATEGORY LINKS PRESENT IN THE SUB_CAT_LINKS FILE AND THEN FINDING THE PRODUCT LINKS FROM THE 
#	PAGE AND INSERTING THEM INTO A SET(scrape_product_links)
# 3. WE GET THE PRODUCT LINKS FROM THE SET ONE BY ONE AND THEN SCRAPE ALL THE INFORMATION NEEDED INCLUDING THE IMAGE DOWNLOADING AND
#	RECOMMENDED PRODUCTS(get_product_info, download_image, full_image, get_recommended_links) 


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import requests
import time
from random import randint
import os
import io
from PIL import Image


options = Options()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

wait = WebDriverWait(driver, 10)

product_counter = 1
##############################       RELATED-PRODUCTS       ##############################################

'''FINDING AND SCRAPING ALL THE RECOMMENDED PRODUCTS OF THE PRODUCT LINK GIVEN, TO DO THIS WE HAVE TO FIRST FIND THE CAROUSEL THAT CONTAINS THE RECOMMENDED PRODUCTS(WHICH IS DIFFERENT FOR DIFFERENT ITEMS) AND THEN FIND THE BUTTON TO THE NEXT PAGE OF THE CAROUSEL(WHICH IS ALSO DIFFERENT FOR DIFFERENT PRODUCTS) AND THEN CLICK THE BUTTON AND SCRAPE ALL THE LINKS UNTIL WE REACH THE END OF THE CAROUSEL '''

def get_recommended_links(link):
	try:
		text1 = driver.find_element(By.XPATH,("//div[contains(@id,'sp_detail')]""//a[@class='a-link-normal']"))
		actions = ActionChains(driver)
		driver.execute_script("arguments[0].scrollIntoView();", text1)			#scrolling down to the carousel
		time.sleep(3)			#cannot use explicit waits because it gives a stale element reference
		unique_texts = set()

		#finding and scraping links in the carousel
		while True:
			text4 = driver.find_elements(By.XPATH,("//div[contains(@id, 'sp_detail')]""//a[@class='a-link-normal']"))
			new_items = False
			pattern = "ie=UTF8&spc="
			for item in text4:
				title = item.text.strip()
				href = item.get_attribute('href')
				if title and href and href not in unique_texts:
					if pattern in href:
						print(f"Title: {title},\n Href: {href}")
						unique_texts.add(href)
						new_items = True
					#	get_product_info(href, product_path)

			if not new_items:						#loop continues until there are no more items
				print("No new items found, stopping the loop.")
				break

			time.sleep(3)
			#finding the button in the carousel
			button = driver.find_element(By.XPATH,("//div[contains(@id,'sp_detail')]""//div[@class='a-carousel-col a-carousel-right']""//a[contains(@id, 'a-autoid-')]"))
			button.click()
			time.sleep(3)

		time.sleep(3)
		product_counter += 1

	except Exception as e:
		print(e)

	return unique_texts
time.sleep(randint(1,5))

###################################    IMAGE - FINDING AND DOWNLOADING    ################################################

'''THERE ARE TWO PARTS 
1.TO FIND THE FULL IMAGE LINK OF THE PRODUCT(full_image)
2.TO DOWNLOAD THE FULL IMAGE THAT WE'VE FOUND OF THE PRODUCT(download_image)-IN HERE THE IMAGE CAN BE OF TWO DIFFERENT TYPES AND BOTH THE CASES NEED TO BE SUPPORTED DIFFERENTLY SO THEY HAVE BEEN HANDLED IN THE IRGBA AND RGB MODE OF THE IMAGE '''

def download_image(download_path, url):
	print(download_path)
	image_content = requests.get(url).content	#using bs4 here to to send a request and download the image from the link we got 			
	image_file = io.BytesIO(image_content)
	image = Image.open(image_file)
	if image.mode != 'RGB':
        	if 'A' in image.getbands():  # Check if the image has an alpha channel
            		image = image.convert('RGBA')
       		else:
            		image = image.convert('RGB')
	with open(download_path, "wb") as f:
		image.save(f, "JPEG")

	print("Success")

def full_image(driver, delay, path, link):
	driver.get(link)
	#print(link)
	image_urls = set()
	
	images = driver.find_elements(By.ID,'landingImage')
	#print(images)
	for image in images:
		img = image.get_attribute('src')
		print(img)
	download_image(path, img)

time.sleep(randint(1,3))

###################################       PRODUCT-INFORMATION           #################################################

'''FINDING AND SCRAPING ALL THE INFORMATION OF THE PRODUCTS THAT ARE PASSED TO THIS FUNCTION VIA THE scrape_product_links FUNCTION'''
'''CREATING AND ENTERING ALL THE INFORMATION INTO SEPARATE FILES AND DIRECTORIES'''
'''FURTHER PASSING THE PRODUCT LINKS TO TWO FUNCTIONS NAMELY full_image(TO DOWNLOAD THE PRODUCT IMAGE) AND get_recommended_products(TO GET THE RECOMMENDED PRODUCTS) '''

def get_product_info(product_link, path):
	global product_counter
	tit = set()

	try:
		driver.get(product_link)

		title = driver.find_element(By.ID, "productTitle")		#scraping title
		print(title.text)
		if title not in tit:
			tit.add(title)			#avoiding duplicate products

			price = driver.find_element(By.CLASS_NAME, "a-price-whole")	#scraping price
			price1 = driver.find_element(By.CLASS_NAME, "a-price-symbol")
			print(price1.text + price.text)


			freqs = set()

			#scraping frequently bought together items
			try:
				freq = wait.until(EC.presence_of_element_located((By.XPATH,"//div[contains(@class,'a-cardui _p13n')]")))
				a_tags = freq.find_elements(By.TAG_NAME, 'a')
				#hrefs = a_tags.get_attribute('href')
				hrefs = [a.get_attribute('href') for a in a_tags]
				for href in hrefs:
					if href and not href.startswith('javascript:void(0)'):
						freqs.add(href)
			except Exception as e:
				print(e)
			print(freqs)

			description1 = ""
			desc = ""
			#scraping description of the product
			try:
				description1 = driver.find_element(By.ID, "productDetails_feature_div").text
			except NoSuchElementException:
				description1 = None

			try:
				desc = driver.find_element(By.ID, "productOverview_feature_div").text
			except NoSuchElementException:
				desc = None

			try:
				d = driver.find_element(By.ID,"detailBulletsWrapper_feature_div").text
			except NoSuchElementException:
				d = None

			product_path = os.path.join(path, "product" + str(product_counter))	#creating product directories
			os.makedirs(product_path, exist_ok=True)

			img_path = os.path.join(product_path, "image.jpg")	#creating files

			file_path = os.path.join(product_path, "product-info")

			#writing into files all the information that is being scraped

			with open(file_path, 'w') as fp:
				fp.write(f"Url: {product_link}\n")
				fp.write("\n")
				print("url written")
				fp.write(f"Title: {title.text}\n")
				fp.write("\n")
				print("title written")
				fp.write(f"Price: {price1.text + price.text}\n")
				fp.write("\n")
				print("price written")
				if description1:
					fp.write(f"Description:\n {description1}\n")
					fp.write("\n")
				elif desc:
					fp.write(f"Description:\n {desc}\n")
					fp.write("\n")
				elif d:
					fp.write(f"Description:\n {d}\n")
					fp.write("\n")
				else:
					fp.write(f"Description: None\n")
					fp.write("\n")
				print("desc written")
				fp.write(f"Frequently Bought Together:\n ")
				for link in freqs:
					fp.write(f"{link}\n")
				fp.write("\n")
				print("freq written")
				fp.write(f"Image Path: {img_path}\n")
				print("img written")

			recommended_links = get_recommended_links(product_link)			#calling get_recommended_links function
			
			if (len(recommended_links)!=0):						#writing recommended links in file
				with open(file_path , "a") as fr:
					fr.write("\n")
					fr.write(f"Recommended Products:\n ")
					for link1 in recommended_links:
						fr.write(f"{link1}\n")
					fr.write("\n")
					print("rec written")

			full_image(driver, 2, img_path, product_link)				#calling full_image function

			product_counter += 1



	except Exception as e:
		print(f"An error occurred: {e}")

time.sleep(randint(1,5))

################################    PRODUCT LINKS    #####################################################

'''FINDING AND SCRAPING ALL THE PRODUCT LINKS THAT ARE AVAILABLE ON THE SUB-CATEGORY PAGES AND THEN PUTTING THEM IN A SET AND PASSING THEM TO THE get_product_info FUNCTION'''

with open("sub_cat_links", "r") as file:
	links = [line.strip() for line in file]

def scrape_product_links(sub_category_link):
	driver.get(sub_category_link)			#getting the chrome page
	print("Sub-category Link:", sub_category_link)
	driver.maximize_window()
	time.sleep(5)
	plinks = set()
	title = driver.find_element(By.XPATH, "//span[contains(@class,'a-size-base a-color-base a-text-bold')]")
	print(title.text)
	sub_cat_dir = '/home/chandni/amazon-final-data2/'+str(title.text)+"/"		#creating the directories and files
	os.makedirs(sub_cat_dir)
	#print(sub_cat_dir)
	ref = "ref=sr_1"								#filtering
	pat = "/gp/"					
	pat1 = "#customerReviews"
	try:
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".s-result-list")))
		product_links = driver.find_elements(By.CSS_SELECTOR, ".s-result-item .a-link-normal")
		for links in product_links:
			link = links.get_attribute("href")
			if pat not in link and pat1 not in link:
				if ref in link:		
					if link not in plinks:
						plinks.add(link)

		for link in plinks:
			get_product_info(link, sub_cat_dir) 
			print("Product Link:",link)
			
	except Exception as e:
		print("Error:", e)

time.sleep(randint(1,3))

for link in links:
	scrape_product_links(link)		#calling the function

######################################    SUB-CATEGORY LINKS    ############################################################

'''FINDING AND SCRAPING THE SUB-CATEGORY LINKS BY OPENING THE MAIN_CAT_LINKS FILE AND SCRAPING ITS INFORMATION ONE-BY-ONE AND THEN ONLY INSERTING THE FIRST TWO SUB-CATEGORY LINKS IN THE sub_cat_links FILE'''

with open("main_cat_links", "r") as file:
	links = [line.strip() for line in file]
	print(links)

def scrape_sub_cat_links(category_link):
	driver.get(category_link)
	print(category_link)
	cclinks = []
	try:
		pat = "%2Cp_n"
		ccat = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID, "s-refinements")))		
		product_class= ccat.find_elements(By.CSS_SELECTOR, "a")
		for link in product_class:
			href = link.get_attribute("href")
			if pat in href:
				if href not in cclinks:
					if href not in cclinks:
						cclinks.append(href)
		fp = os.open("sub_cat_links",os.O_CREAT | os.O_APPEND | os.O_RDWR)
		os.write(fp,str.encode(cclinks[0]))
		os.write(fp,str.encode('\n'))
		os.write(fp,str.encode(cclinks[1]))
		os.write(fp,str.encode('\n'))
		os.close(fp)
		print("HAHA: ",cclinks[0])
		

	except Exception as e:
			print(e)

#for link in links:
#	scrape_sub_cat_links(link)



