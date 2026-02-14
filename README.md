# 🛒 Automated Amazon Scraper with Image Processing

---
---

## 📚 Table of Contents

- 🧾 [Overview](#overview)
- 🔄 [Execution Flow](#execution-flow)
- 🛠️ [Technologies Used](#technologies-used)
- 📁 [Project Structure](#project-structure)
- ⚙️ [Workflow](#workflow)
- 🚀 [Features](#features)
- 🧰 [Requirements & Installation](#requirements--installation)
- 🎯 [Usage](#usage)
- 📦 [Output Structure](#output-structure)
- 🔮 [Enhancement Opportunities](#enhancement-opportunities)

---


## 🧾 Overview

This project is an end-to-end automated web scraping system designed to extract structured product data from Amazon using browser automation and dynamic page interaction techniques.

The scraper performs multi-level navigation starting from main categories, drilling down into subcategories, collecting product-level data, downloading associated images, and organizing all outputs into a scalable hierarchical directory structure.

It integrates Selenium-based automation, dynamic DOM handling, intelligent filtering of product links, and image processing workflows to create a structured and reusable dataset.

The system is designed to simulate large-scale automated data collection pipelines used in e-commerce analytics, competitor monitoring, and catalog intelligence systems.

---

## 🔄 How the Project Works (Execution Flow)

The project operates in multiple stages:

### Stage 1: Main Category Extraction (`main_links.py`)
1. Launch automated browser session  
2. Navigate to Amazon homepage  
3. Extract visible main category links  
4. Filter irrelevant patterns  
5. Store cleaned category links in `main_cat_links` file  

### Stage 2: Subcategory & Product Scraping (`scrape.py`)

#### Stage 2A: Subcategory Link Extraction
1. Read `main_cat_links`  
2. Open each category page  
3. Extract filtered subcategory links  
4. Store selected subcategory links in `sub_cat_links`  

#### Stage 2B: Product Link Extraction
1. Open each subcategory page  
2. Identify valid product result items  
3. Filter navigation and review-only links  
4. Store unique product links in a set  
5. Pass product links to product processing function  

#### Stage 2C: Product Data Extraction
For each product link:
1. Extract product title  
2. Extract product price  
3. Extract product description (multiple fallback strategies)  
4. Extract “Frequently Bought Together” links  
5. Extract recommended product carousel links  
6. Create dedicated product directory  
7. Write structured information into product-specific file  
8. Download and process product image  
9. Store image inside product folder  

#### Stage 2D: Image Processing
1. Identify full-resolution product image  
2. Download image via HTTP request  
3. Handle RGB and RGBA image formats  
4. Convert and save as standardized JPEG  

---

## 🛠️ Technologies Used

### Core Automation
- Selenium WebDriver  
- ChromeDriver (managed via `webdriver-manager`)  
- ActionChains  
- WebDriverWait & ExpectedConditions  

### Web Handling
- Dynamic DOM navigation  
- CSS Selectors  
- XPath locators  
- URL filtering logic  

### Data Handling
- Python file handling  
- OS module for directory creation  
- Set-based duplicate removal  

### Image Processing
- `requests`  
- `Pillow (PIL)`  
- RGB / RGBA detection  
- JPEG standardization  

### Supporting Libraries
- `time`  
- `random`  
- `io`  

---

## 📁 Project Structure

```
Amazon-Scraper/
│
├── main_links.py
├── scrape.py
├── requirements.txt
└── screenshots/
```

### main_links.py
- Opens Amazon homepage  
- Extracts visible main category links  
- Filters unwanted patterns  
- Stores valid links into `main_cat_links`  

### scrape.py
Core scraping engine responsible for:
- Subcategory extraction  
- Product link extraction  
- Product data scraping  
- Image downloading  
- Recommended product scraping  
- Folder and file creation  

### requirements.txt
Contains required external dependencies.

---

## ⚙️ Workflow (Nested Execution Logic)

### Stage 1: Extract Main Categories
1. Open Amazon homepage  
2. Extract navigation bar categories  
3. Filter unwanted URLs  
4. Store clean category links  

### Stage 2: Extract Subcategories
1. Iterate through each main category  
2. Open category page  
3. Extract valid subcategory filter links  
4. Store selected subcategory links  

### Stage 3: Extract Product Links
1. Iterate through each subcategory  
2. Load results page  
3. Identify valid product result items  
4. Filter review-only and navigation links  
5. Store unique product links in a set  

### Stage 4: Product-Level Scraping
1. Iterate through each unique product link  
2. Open individual product page  
3. Extract product title  
4. Extract product price  
5. Extract product descriptions (multiple fallback selectors)  
6. Extract “Frequently Bought Together” links  
7. Extract recommended carousel product links  
8. Download full-resolution product image  
9. Create product-specific directory  
10. Store structured product data  

### Stage 5: Image Processing
1. Fetch product image using `requests`  
2. Load image into memory using `Pillow`  
3. Detect image mode (RGB / RGBA)  
4. Convert format if required  
5. Standardize image to JPEG format  
6. Save processed image to product directory  

---

## 🚀 Features

- Multi-level scraping pipeline  
- Automated ChromeDriver management  
- Explicit waits for stability  
- Dynamic carousel navigation  
- Intelligent URL filtering  
- Duplicate product avoidance  
- Hierarchical directory generation  
- Structured product-level storage  
- RGB/RGBA image format handling  
- Recommended product extraction  
- Frequently bought together extraction  

---

## 🧰 Requirements & Installation

### Prerequisites
- Python 3.10+  
- Google Chrome browser installed  

### Clone Repository
```
git clone <your-repo-link>
cd Amazon-Scraper
```

### Install Dependencies
```
pip install -r requirements.txt
```

### Run the Scraper

Step 1:
```
python main_links.py
```

Step 2:
```
python scrape.py
```

---

## 🎯 Usage

This project can be used for:
- E-commerce price monitoring  
- Competitor product analysis  
- Dataset generation for analytics  
- Image dataset creation  
- Product catalog building  
- Market trend research  

The hierarchical output structure allows easy conversion into CSV or JSON for further data analysis.

---

## 📦 Output Structure

```
output/
 └── <Category_Name>/
      ├── product1/
      │     ├── product-info
      │     └── image.jpg
      │
      ├── product2/
      │     ├── product-info
      │     └── image.jpg
      │
      └── ...
```

Each product folder contains:
- Structured product information file  
- Downloaded processed image  
- Recommended product links  
- Frequently bought together links  

(Screenshots will be added here)

---

## 🔮 Enhancement Opportunities

- Implement proxy rotation  
- Add CAPTCHA handling  
- Introduce logging system  
- Convert product-info files to JSON  
- Store data in SQLite or PostgreSQL  
- Add headless browser mode  
- Implement multithreading for performance  
- Add CLI-based category selection  
- Add dashboard visualization layer  
- Add retry logic for network failures  

---
