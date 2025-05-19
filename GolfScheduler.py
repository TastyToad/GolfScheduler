from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import calendar
import logging
import subprocess



#Configureing logging 
log = logging.getLogger("test")
log.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
log.addHandler(ch)




# Suppress Chrome logs ,official documentation is depreciated
def get_options():
    options = Options()
    options.add_argument("--log-level=3") 
    return options

#Set Driver with options
def get_driver(options):
    driver = webdriver.Chrome(options=options)
    return driver

def set_wait(driver):
    wait = WebDriverWait(driver, timeout=2)   
    return wait

#Open the starting page
def open_page(driver):
    driver.get("https://sccharlestonweb.myvscloud.com/webtrac/web/search.html?module=GR&Search=no")
    time.sleep(1)
    log.info("page open")

#Change the player count to 3
def change_player_count(driver , wait): #add possible iterations over this for futere, might not be needed as 1 person views all open slots  but this is only for 3 at the moment

     #Click drop down box
     log.info("Changing player count")
     log.info("Clicking player change button")
     wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="numberofplayers_vm_1_button"]')))  
     driver.find_element(By.XPATH, '//*[@id="numberofplayers_vm_1_button"]').click()
     log.info("Button selected")

     #Click on 3 
     log.info("Changing players to 3")
     time.sleep(1)
     wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="numberofplayers_vm_1_wrap"]/div/ul/li[3]')))  
     driver.find_element(By.XPATH, '//*[@id="numberofplayers_vm_1_wrap"]/div/ul/li[3]').click()
     time.sleep(1)
     log.info("3 players selected")
 
     

def select_tee_time(driver,wait):   #Completely working needs no edit

    #Select Time Box
    log.info("Selecting begin time box")
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="grwebsearch_nextgengroup1"]/div[1]/div[3]/button')))  
    driver.find_element(By.XPATH, '//*[@id="grwebsearch_nextgengroup1"]/div[1]/div[3]/button').click()
    time.sleep(1)
    
    #Expand Drop down menu
    log.info("Selecting time drop-down box")
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="begintime_vm_3_wrap"]/button')))  
    driver.find_element(By.XPATH, '//*[@id="begintime_vm_3_wrap"]/button').click()
    time.sleep(1)

    #Select Time
    log.info("Selecting 7:00 am")#it shows all times avaliable after the lowest starting time, this is the easiest way to find all avaliable to avoid itteratign times
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[text()="07:00 am"]')))  
    driver.find_element(By.XPATH, '//*[text()="07:00 am"]').click()
    time.sleep(1)



def select_date(driver,wait,saturday):  #needs to be able to itterate over saturdays create callendar func and iterate the retuned times
     
    #Select Date Button
    log.info("Attempting to click drop-down button")
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="grwebsearch_nextgengroup1"]/div[1]/div[2]/button')))      
    driver.find_element(By.XPATH, '//*[@id="grwebsearch_nextgengroup1"]/div[1]/div[2]/button').click()
    log.info("Drop-down button clicked")
      
    #Select Callendar Drop Down grid
    log.info("Attempting to click calendar drop-down")
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="begindate_vm_2_button"]')))    
    driver.find_element(By.XPATH, '//*[@id="begindate_vm_2_button"]').click()
    time.sleep(1)
    log.info("Calendar clicked")

    #Select date : 17th    needs eddit with calendar function for saturdays ,  pass date of saturdays into function,  select matching text in html,   run for each matching ,, 
    log.info("Attempting to select date")
    try:
        driver.find_element(By.XPATH, f"//*[normalize-space(text())='{saturday}']").click()
    except:
         driver.find_element(By.XPATH, '//*[@id="begindate_vm_2_wrap"]/button').click()
   
    
    time.sleep(1)        
    log.info("Date selected")

def get_dates():
    today = datetime.date.today()
    end_date = today + datetime.timedelta(days=31)
    current = today 

    saturdays = []

    while current <= end_date:
        saturdays.append(current.strftime("%d"))
        current += datetime.timedelta(days=7)
    
    return saturdays
  


def check_tee_times(driver,wait):
    
    #Select search button
    log.info("Selecting search button")
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="grwebsearch_buttonsearch"]')))  
    driver.find_element(By.XPATH, '//*[@id="grwebsearch_buttonsearch"]').click()
    time.sleep(1)


def get_results(driver,wait):

    #stores and prints the results. , needs the ability to store the data that will come from a sucesssfull multiple runs
    log.info("Results time...\n")
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="grwebsearch_noresultsmessage"]')))  
    text = driver.find_element(By.XPATH, '//*[@id="grwebsearch_noresultsmessage"]').text
    log.info(text)

    
        
    # use positive time outputs to update an ics and subscribe an outlook callendar too it so that it will sync and change , 




# Run the job
options = get_options()
driver = get_driver(options)
wait = set_wait(driver)
open_page(driver)
saturdays = get_dates()

for saturday in saturdays:
    print (saturday)
    change_player_count(driver , wait)
    select_tee_time(driver,wait)
    select_date(driver,wait,saturday)
    check_tee_times(driver , wait)
    get_results(driver,wait)



driver.quit()