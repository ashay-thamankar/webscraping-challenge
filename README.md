# Car Data Scraping

This README file provides an overview of the process used to scrape car data from the CarWale website, convert it to JSON format, and outlines the next steps in the project.

## Overview

We utilized Selenium WebDriver with Chrome to scrape data from the Maruti Suzuki Fronx page on the CarWale website.

## Data Scraped

We scraped the following data from the website:

- Car name
- Overview
- Variants
- Specifications
- Key Features
- Summary
- Pros and Cons

## How Data was Scraped

1. Selenium WebDriver with Chrome was used to automate the browsing process.
2. We navigated to the Maruti Suzuki Fronx page ([link](https://www.carwale.com/maruti-suzuki-cars/fronx/)) to extract the desired data.
3. The data was extracted from the webpage using XPath and other relevant locators.
4. The extracted data was then processed and converted into a dictionary format.
5. Finally, the dictionary was converted to a JSON file for further analysis and storage.

## Screenshots

- Screenshot of the CarWale website homepage:
![CarWale Website Homepage](https://github.com/ashay-thamankar/webscraping-challenge/raw/main/screenshots/carwale%20website.png)

- Screenshot of the scraped JSON data viewer:
![Scraped JSON Data Viewer](https://github.com/ashay-thamankar/webscraping-challenge/raw/main/screenshots/web%20scraped%20data%20json%20view.png)

## Next Steps

The next steps in the project involve:

1. Crawling to the variants pages and scraping additional data.
2. Extracting reviews from the variants pages.
3. Analyzing the sentiment of each review.
4. Any further analysis or visualization of the data as required.

Stay tuned for updates on our progress!
