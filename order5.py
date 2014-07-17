from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip
import csv
import string
import contextlib
def get_text_excluding_children(driver, element):
    return driver.execute_script("""
    return jQuery(arguments[0]).contents().filter(function() {
        return this.nodeType == Node.TEXT_NODE;
    }).text();
    """, element)
######launch firefox
driver = webdriver.Firefox()
######open config file
with open("config.txt","rb") as configfile:
    text = configfile.readlines()

    email=text[0].strip()
    pw=text[1].strip()
    rowcount=int(text[2])
    startline=int(text[3])

    print email
    print startline
######open autoorder file
with open("autoorder.csv","rb") as csvfile:
#with open('autoorder.csv', 'rb') as csvfile:
  order = csv.reader(csvfile, delimiter=',', quotechar='|')

  #for row in order:
    #rowcount=rowcount+1
  print "rowcount:",rowcount
  lines = csvfile.readlines()
  for line in range (startline,rowcount+1):
    print "line:",line
    #csvfile.seek(line)
    row = lines[line].split(',')
    print row
    FullName = row[0]
    AddressLine1 = row[1]
    City = row[2]
    State = row[3]
    Zip = row[4]
    Link = row[5]
    print Link
    speed = row[6]
    quantity = row[7]
######open product page
    driver.get(Link)
######add to cart
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "add-to-cart-button"))
        )
        element.click()
    except TimeoutException,e:

        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "bb_atc_button"))
        )
        element.click()
    finally:
        print "login in"



    #driver.implicitly_wait(1)

    #driver.find_element_by_id("add-to-cart-button").click()

    driver.implicitly_wait(5)

    #submit.addToCart
    try:
        element = driver.find_element_by_xpath("//input[@value = 'addToCart']")
        print "find addToCart"
        driver.find_element_by_xpath("//input[@value = 'addToCart']").click()
    except NoSuchElementException,e:
        print "can't find addToCart"
    try:
        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']"))
        )
    finally:
        print "find login"
    inputs = driver.find_elements_by_xpath("//input[@type='checkbox']")[0].click()

    buybook = driver.find_element_by_class_name("hlb-item-title")
    booktitle = get_text_excluding_children(driver,buybook)
    print booktitle
    driver.find_element_by_link_text("Proceed to checkout").click()
    driver.implicitly_wait(5)
    try:
        driver.find_element_by_link_text("Proceed to checkout").click()
    except NoSuchElementException,e:
        print "checkout"
    finally:
        print "checkout"


    driver.implicitly_wait(10)

    try:
        driver.find_element_by_id("ap_email").clear()
        driver.find_element_by_id("ap_email").send_keys(email)
        driver.find_element_by_id("ap_password").send_keys(pw)
        driver.find_element_by_id("signInSubmit-input").click()
    except NoSuchElementException,e:
        print "already login"
    finally:
        print "find address"

    driver.implicitly_wait(10)
    try:
        driver.find_element_by_id("message_error")
        driver.find_element_by_id("ap_email").clear()
        driver.find_element_by_id("ap_email").send_keys(email)
        driver.find_element_by_id("ap_password").send_keys(pw)
        driver.find_element_by_id("signInSubmit-input").click()
    except NoSuchElementException,e:
        print "already login"
    finally:
        print "relogin"
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "a-container"))
        )
    except TimeoutException,e:
        driver.quit()
        print "close page, restart"
    finally:
        print "find address"


    driver.find_element_by_id("enterAddressFullName").send_keys(FullName)
    driver.find_element_by_id("enterAddressAddressLine1").send_keys(AddressLine1)
    driver.find_element_by_id("enterAddressAddressLine2").send_keys("")
    driver.find_element_by_id("enterAddressCity").send_keys(City)
    driver.find_element_by_id("enterAddressStateOrRegion").send_keys(State)
    driver.find_element_by_id("enterAddressPostalCode").send_keys(Zip)
    driver.find_element_by_id("enterAddressPhoneNumber").send_keys("6463209993")
    driver.implicitly_wait(15)
    driver.find_element_by_name("shipToThisAddress").click()

    driver.implicitly_wait(5)
    try:
        element = driver.find_element_by_xpath("//input[@value = 'addr_0']")
        print "use original address"
        driver.find_element_by_xpath("//input[@value = 'addr_0']").click()
        try:
            element = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='submit']"))
            )
            driver.find_elements_by_xpath("//input[@type='submit']")[0].click()
        finally:
            print "confirm address continue"
    except NoSuchElementException,e:
        print "no suggested address"


    driver.implicitly_wait(5)

    driver.find_element_by_id("includeMessageCheckbox-0").click()
    message = driver.find_element_by_id("message-area-0")
    message.clear()
    driver.implicitly_wait(5)
    message.send_keys("Enjoy your product!")

    driver.find_elements_by_xpath("//input[@type='submit']")[0].click()
    print "gift option continue"
    driver.implicitly_wait(5)

    try:
        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ship-speed"))
        )

        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='submit']"))
        )
        driver.find_elements_by_xpath("//input[@type='submit']")[0].click()
    finally:
        print "shipping continue"

    driver.implicitly_wait(20)


    try:
        element = WebDriverWait(driver, 500).until(
            EC.presence_of_element_located((By.ID, "continue-top"))
        )
        driver.find_element_by_id("continue-top").click()
    except NoSuchElementException,e:
        print "no card continue"
    finally:
        print "card continue"

    driver.implicitly_wait(10)



    try:
        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "displayAddressFullName"))
        )
    finally:
        print "find address"

    #action = webdriver.ActionsChains(firefox)
    #action.move_to_element(address).perform()
    #action.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
    #address.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
    #driver.implicitly_wait(5)
    #address.send_keys(Keys.CONTROL, 'c')
    #driver.implicitly_wait(5)
    #info = pyperclip.getcb()
    address1 = driver.find_element_by_class_name("displayAddressFullName")
    post_name = get_text_excluding_children(driver,address1)
    print post_name
    address2 = driver.find_element_by_class_name("displayAddressAddressLine1")
    street = get_text_excluding_children(driver,address2)
    print street
    address3 = driver.find_element_by_class_name("displayAddressCityStateOrRegionPostalCode")
    region = get_text_excluding_children(driver,address3)
    print region
    address5 = driver.find_element_by_class_name("displayAddressPhoneNumber")
    phonenumber = get_text_excluding_children(driver,address5)
    print phonenumber
    if(post_name!=FullName):
        print "name is wrong"
        #driver.quit()

    driver.find_element_by_class_name("change-quantity-button").click()
    driver.implicitly_wait(5)
    try:
        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "quantity-input"))
        )
        driver.find_element_by_class_name("quantity-input").send_keys(quantity)
    finally:
        print quantity

    if quantity>1:
        driver.implicitly_wait(15)
        try:
            element = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CLASS_NAME, "update-quantity-button"))
            )
            driver.find_element_by_class_name("update-quantity-button").click()
            driver.implicitly_wait(15)
            driver.find_element_by_class_name("update-quantity-button").click()
        except ElementNotVisibleException,e:
            print "changed"
        finally:
            print "change quantity"

    driver.implicitly_wait(1000)
    try:
        #element = WebDriverWait(driver, 100).until(
        #    EC.element_to_be_clickable((By.CLASS_NAME, "change-quantity-button']"))
        #)
        #total = driver.find_element_by_class_name("grand-total-price")
        #totalprice = total.find_elements_by_xpath('./*')
        #totalpricestring = float(string.replace(totalprice[0].text,"$",""))*float(quantity)
        total = driver.find_elements_by_class_name("a-align-bottom")
        totalprice = total[-3]
        totalpricestring = float(string.replace(totalprice.text,"$",""))*float(quantity)
        print totalpricestring

    finally:
        print "total price"




    driver.find_element_by_name("placeYourOrder1").click()
    driver.implicitly_wait(10)
    try:
        driver.find_element_by_name("placeYourOrder1").click()
    except NoSuchElementException,e:
        print "order placed"
    finally:
        print "order placed"

    driver.implicitly_wait(10)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "shipment"))
        )
    finally:
        print "order complete"
    order=driver.find_element_by_class_name("shipment")
    ordernum = order.find_elements_by_xpath('./*')
    ordernumstring = ordernum[0].text
    print ordernumstring


    with open("placeorder.csv","a") as csvfile1:
        resultwriter = csv.writer(csvfile1, delimiter=',')
        #csvfile1.seek(line)
        #row=csvfile1.write(csvfile1)
        row[0]=FullName
        row[1]=AddressLine1
        row[2]=City
        row[3]=State
        row[4]=Zip
        row[5]=booktitle
        row[6]=Link
        row[7]=""
        row[7]=totalpricestring
        row[8]=""
        row[9]=ordernumstring
        resultwriter.writerow(row)