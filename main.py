# Web scraping of car related data from carwale.com

# importing necessary libraries
import time
from selenium import webdriver
from selenium.common import ElementClickInterceptedException, StaleElementReferenceException, \
    ElementNotInteractableException
from selenium.webdriver.common.by import By
import json

car_url = 'https://www.carwale.com/maruti-suzuki-cars/fronx/'
driver = webdriver.Chrome()

driver.get(car_url)

# Name of the car
car_name = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[2]/div/div[1]/div/div/h1')
car_name = car_name.text

# Adding delay if there is slow internet connection
time.sleep(1)

# Click on overview cell
overview_origin  = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[3]/div[1]/div/ul[1]/li[1]/div')
overview_origin.click()
time.sleep(2)

# Scraping price range
price_range = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[4]/div[2]/div[2]/div[1]/span')
price_range = price_range.text.replace('-', 'to')

time.sleep(2)

# Clicking on more named button for crossdown
driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[3]/div[1]/div/ul[1]/li[4]/div/span').click()
time.sleep(2)
driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[5]/div[1]/div[1]/div[4]/div/section/div/div/div/div[2]').click()
time.sleep(2)
launch_date = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[5]/div[1]/div[1]/div[4]/div/section/div/div/div/div[1]/div/div[2]/p[2]').text.split('on')[-1].strip().split('.')[0]

time.sleep(2)

# Scraping varient data
varient = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[5]/div[1]/div[1]/div[4]/div/section/div/div/div/div[1]/div/div[2]/p[4]').text.split('-')[-1].split('.')[0].split('variants –')[-1].strip()

pro_p = driver.find_elements(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[5]/div[1]/div[1]/div[7]/div/section/div[2]/div[1]/ul/li[1]/div/div/ul')
pro_p = [pro.text for pro in pro_p][0].split('\n')

# Adding into a dictionary
overview_dict = {}
overview_dict['Price Range'] = price_range
overview_dict['Launch Date'] = launch_date
overview_dict['Varients'] = varient
overview_dict['Key Selling Points'] = pro_p

# Adding into a main dictionary
dict_1 = {}
dict_1['Overview'] = overview_dict

varients_list = []

details = {}
varient_data = driver.find_elements(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[5]/div[1]/div[1]/div[1]/div[1]/section/div/div[2]/table/tbody')
time.sleep(4)

# Adding try block if there any non clickable found
try:
    temp_to_click = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[5]/div[1]/div[1]/div[1]/div[1]/section/div/div[2]/div')
    time.sleep(2)
    temp_to_click.click()
except ElementNotInteractableException:
    temp_to_click = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[5]/div[1]/div[1]/div[1]/div[1]/section/div/div[2]/div')
    time.sleep(2)
    temp_to_click.click()
except ElementClickInterceptedException:
    pass
time.sleep(2)

# Looping to get the varient data
for var in varient_data:
    nm = driver.find_elements(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[5]/div[1]/div[1]/div[1]/div[1]/section/div/div[2]/table/tbody')[0].text.split('\nAdd to compare\nShow price in my cityGet Offers\n')
    print('nm print')
    print(nm)
    for n in nm:
        new_list = n.split('\n') 
    
        temp_v = new_list[1].split(',')
        details = {
        'Engine': ','.join(temp_v[:3]),
        'Mileage': temp_v[3],
        'Power': temp_v[4],
        'Price': new_list[-1]
        }
        varient_dict_t = {
            "Name": new_list[0],
            "Details": details
        }
        varients_list.append(varient_dict_t)
dict_1['Varients'] = varients_list

# Scraping the specification data
speci_list = driver.find_elements(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[5]/div[1]/div[1]/div[2]/div/section/div/div/table/tbody')

speci_list = [n.text for n in speci_list]
speci_list = speci_list[0].split('\n')
speci_dict = {}
key = [speci_list[i] for i in range(len(speci_list)) if i % 2 == 0 and i != 0]
val = [speci_list[i] for i in range(len(speci_list)) if i % 2 != 0 and i != 1]

for i in range(len(key)):
    speci_dict[key[i]] = ','.join(val[i].split('&'))

dict_1['Specifications'] = speci_dict

# Scraping the key features data
key_feature = driver.find_elements(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[5]/div[1]/div[1]/div[3]/section/div/div/div[1]/div/ul')
key_feature_list = [ke.text for ke in key_feature][0].split('\n')
dict_1['Key Features'] = key_feature_list

feature1 = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[5]/div[1]/div[1]/div[4]/div/section/div/div/div/div[1]/div/div[2]/p[6]').text
feature2 = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[5]/div[1]/div[1]/div[4]/div/section/div/div/div/div[1]/div/div[2]/p[7]').text
features_all = feature1 + '\n' + feature2

# Scraping the summary data
summary_dict = {
    'Price': price_range.replace('to', '-') ,
    'Features': features_all
}
dict_1['Summary'] = summary_dict

# Scraping the pro and cons data
pro_list = driver.find_elements(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[5]/div[1]/div[1]/div[7]/div/section/div[2]/div[1]/ul/li[1]/div/div/ul')
cons_list  = driver.find_elements(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[5]/div[1]/div[1]/div[7]/div/section/div[2]/div[1]/ul/li[2]/div/div/ul')
pro_l = [pro.text for pro in pro_list][0].split('\n')
cons_l = [con.text for con in cons_list][0].split('\n')
pro_con_dict = {'Pros': pro_l, 'Cons': cons_l}
dict_1['Pros and Cons'] = pro_con_dict

# Scraping the review with its description
review_list_ele = driver.find_elements(by=By.XPATH, value='/html/body/div[2]/div[2]/div[1]/div[5]/div[1]/div[1]/div[12]/div[2]/div/section/div/div[1]/ul')

review = [review.text for review in review_list_ele]
review = [rev.split('\n') for rev in review][0]

review_list = [{'title': review[n], 'description': review[n+1] } for n in range(len(review)) if n % 6 ==0]

dict_1['Reviews'] = review_list

# Adding all the scraped data into a dictionary
final_dict  = {f'{car_name}': dict_1}

print(final_dict)

# Saving as a json file
filename = 'car_data.json'
with open(filename, 'w') as f:
    json.dump(final_dict, f, indent=4)
print(f"Data saved at {filename}")

# Closing the driver file
driver.close()
driver.quit()