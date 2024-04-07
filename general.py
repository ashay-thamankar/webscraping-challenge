# Web scraping of car related data from carwale.com given any link

# importing necessary libraries
import time
from selenium import webdriver
from selenium.common import ElementClickInterceptedException, StaleElementReferenceException, \
    ElementNotInteractableException, NoSuchElementException,TimeoutException
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# car_url = 'https://www.carwale.com/maruti-suzuki-cars/fronx/'
# car_url = 'https://www.carwale.com/tata-cars/punch-ev/'
# car_url = 'https://www.carwale.com/kia-cars/sonet/'
car_url = 'https://www.carwale.com/hyundai-cars/creta-n-line/'

driver = webdriver.Chrome()

driver.implicitly_wait(2)

final_dict = {}
inter_dict = {}

driver.get(car_url)

time.sleep(1)

# Name of the car
car_name = driver.find_element(By.CSS_SELECTOR, '.o-cKuOoN h1')
car_name = car_name.text

price_range = driver.find_element(By.CSS_SELECTOR, 'span.o-Hyyko')
price_range = price_range.text.replace('-', 'to')

time.sleep(2)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight/5);")

time.sleep(3)

# click on read more to expand the drop down and scrape the launch date
try:
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.o-fznJDS.o-ckGLSv.o-fznJFI.o-cMwvCl.o-fzpihY.o-fzpilm.o-brXWGL div.o-frwuxB.o-eqqVmt.o-eemiLE.o-cHfWwD.o-fyWCgU.o-fzoTov.o-elzeOy'))
    )
    print("Element found!")
    # Click on the element
    element.click()
except TimeoutException:
    print("Timeout: Element not found within 5 seconds")

time.sleep(2)

# To scrape the launch date from sumamry block
summary = driver.find_elements(By.CSS_SELECTOR, 'div.vDnuC_ p')
time.sleep(2)

launch_date = summary[1].text.split(' on ')[-1].replace('.','')

time.sleep(2)

varients = ''
# To find varients in car
## The varient is not in a common place. So we need to check the varient word and fetch the next sentense
for i in range(len(summary)):
    temp = summary[i].text.replace(':','').lower().split() # varients have in different rows so search varient key and its next row is its varients
    if 'variants' in temp:
        varients = summary[i+1].text
        break


inter_dict['Overview'] = {
    'Price Range': price_range,
    'Launch Date': launch_date,
    'Varients': varients
}
time.sleep(2)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight/9);")
# To get the diferent car varients
time.sleep(2)
try:
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.o-fzptVd.o-fzptYr.o-frwuxB.o-tvvmc.o-elzeOy.o-bkmzIL.o-djSZRV.o-eCFISO.o-YCHtV'))
    )
    print("Element found!")
    # Click on the element
    element.click()
except TimeoutException:
    print("Timeout: Element not found within 5 seconds")
# driver.find_element(By.CSS_SELECTOR, 'div.o-fzptVd.o-fzptYr.o-frwuxB.o-tvvmc.o-elzeOy.o-bkmzIL.o-djSZRV.o-eCFISO.o-YCHtV').click()
time.sleep(2)
varient_list = driver.find_elements(By.CSS_SELECTOR, 'tbody.o-dJmcbh tr')
var_out_list = []
for var in varient_list:
    try:
        name_var = var.find_element(By.CSS_SELECTOR, 'a.o-eZTujG.o-jjpuv.o-cVMLxW')
        time.sleep(2)
        details_var = var.find_element(By.CSS_SELECTOR, 'span.o-cpNAVm')
        time.sleep(2)
        price_var = var.find_element(By.CSS_SELECTOR, 'div.o-jjpuv.o-eqqVmt.o-dJmcbh.o-fzpilz span')
        time.sleep(3)
        engine = ','.join(details_var.text.split(',')[:3])
        if len(details_var.text.split(',')) == 5:
            power = details_var.text.split(',')[-1]
            mileage = details_var.text.split(',')[-2]
        else:
            tem = details_var.text.split(',')[-1].split(' ')
            if 'bhp' in tem:
                power = details_var.text.split(',')[-1]
                mileage = 'NA'
            else:
                mileage = details_var.text.split(',')[-1]
                power = 'NA'
        var_temp_dict = {
            'Name': name_var.text,
            'Details': {'Engine': engine,
                        'Mileage': mileage,
                        'Power': power,
                        'Price': price_var.text
            }
        }
  
        var_out_list.append(var_temp_dict)
    except NoSuchElementException:
        pass

time.sleep(3)

# all the varient are added to the dictionary
inter_dict['Variants'] = var_out_list

# Specification scraping 
## The problem is all cars do not have specific specification for each car

time.sleep(2)
specification_list = driver.find_elements(By.CSS_SELECTOR, 'table.o-bfyaNx.o-dJmcbh.o-dKUdmM.o-cpnuEd tr')
speci_dict = {}
for specification in specification_list:
    first = specification.find_element(By.CSS_SELECTOR, 'span.o-cpNAVm.o-KxopV.o-byFsZJ').text
    second = specification.find_element(By.CSS_SELECTOR, 'td.o-eqqVmt.o-eemiLE.o-cYdrZi.o-eYokMk').text
    speci_dict[first] = second
 
inter_dict['Specifications'] = speci_dict

# key features

try:
    element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.o-frwuxB.o-cHfWwD.o-KxopV.o-cQa-DfF.o-eqqVmt.o-bdcqQZ.o-fzfPNY.o-elzeOy'))
)
    print("Element found!")
    # Click on the element
    element.click()
    time.sleep(2)
    feature_list = driver.find_elements(By.CSS_SELECTOR, 'ul.o-bkmzIL.o-fyWCgU.o-cpNAVm.o-fBkfen.o-fznVqX li')
    features = [fea.text for fea in feature_list]
except TimeoutException:
    features = ['feature list not found in website']
    print("Timeout: Element not found within 5 seconds")
except NoSuchElementException:
    features = ['feature list not found in website']
except:
    features = ['feature list not found in website']

inter_dict['Key Features'] = features

# summary

try:
    time.sleep(2)
    pro_list = driver.find_elements(By.CSS_SELECTOR, 'div.o-fznJPk.o-eqYUlK ul.o-czsMOo.o-cOtEaW.o-bsCSvY.o-efHQCX.o-bklwfk li.o-dueWSB.o-fznJPp.o-bifPsq.o-cglRxs.o-fznJDS.o-ckGLSv.o-fznJFI.o-cMwvCl div.o-bkmzIL.o-cpNAVm.o-fznJDS.o-fzoTtm.o-chNNuk.ZBVXSc.dcJ_VH ul li')
    pros = [p.text for p in pro_list]                               

    time.sleep(2)
    cons_list = driver.find_elements(By.CSS_SELECTOR, 'div.o-fznJPk.o-eqYUlK ul.o-czsMOo.o-cOtEaW.o-bsCSvY.o-efHQCX.o-bklwfk li.o-cglRxs.o-fznJDS.o-ckGLSv.o-fznJFI.o-cMwvCl div.o-bkmzIL.o-cpNAVm.o-fznJDS.o-fzoTtm.o-chNNuk.ZBVXSc.dcJ_VH ul li')
    cons = [c.text for c in cons_list][len(pros):]                                                             

except:
    pros = 'Pros not found on website'
    cons = 'Cons not found on website'


inter_dict['Pros and Cons'] = {'Pros': pros, 'Cons': cons}

review_l = driver.find_elements(By.CSS_SELECTOR, 'div.o-dJmcbh.o-bqHweY.o-BosvO.o-wuqlZ.o-dgwiHy.o-fBNTVC ul li')

review_li = [r.text for r in review_l]

review_list = []
for re in review_l:
    time.sleep(2)
    heading = re.find_element(By.CSS_SELECTOR, 'div.o-fznJPk div.o-bqHweY.YB0sNd.o-bfyaNx.o-bNxxEB.o-jjpuv.o-dqVwuv.o-byFsZJ.o-dsJzhG.o-eZTujG')
    time.sleep(1)
    heading = heading.text
    time.sleep(2)
    body = re.find_element(By.CSS_SELECTOR, 'div.o-fznJPk div.undefined.o-brXWGL div.o-eZTujG.o-bkmzIL.o-fyWCgU.undefined')
    time.sleep(1)
    body = body.text
    review_dict = {
        'Title':heading,
        'Body': body
    }

    review_list.append(review_dict)

inter_dict['Reviews'] = review_list
final_dict[car_name] = inter_dict

print(final_dict)


# Saving as a json file
filename = 'any_car_data.json'
with open(filename, 'w') as f:
    json.dump(final_dict, f, indent=4)
print(f"Data saved at {filename}")

# Closing the driver file
driver.close()
driver.quit()
