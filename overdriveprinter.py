#Or use the context manager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import mmap
import numpy as np
import schedule
import time
import json
import os
import filecmp
import shutil
import glob

#the current book id to download
book_ID = "XXXXXXX"
directory = "/Users/josephparampathu/Desktop/Programming/OverdriveFiles/" + str(book_ID)
try:
    os.makedirs(directory)
except:
    pass

# Sets the selenium driver and ChromeOptions for printing
settings = {
    "recentDestinations": [{
        "id": "Save as PDF",
        "origin": "local",
        "account": ""
    }],
    "selectedDestinationId": "Save as PDF",
    "version": 2
}
prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings), 'savefile.default_directory': directory}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--kiosk-printing')
driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))


# Overdrive credentials, password, account; login to OCPLL page
account = "XXXXXXX"
password = "XXXXXXX"
driver.get("https://lexisdl.com/welcome/login/ocpll?origination=/library/ocpll/open")

#wait for page to load
time.sleep(2)

#ensure correct page
if (driver.title != 'Welcome | LexisNexis Digital Library'):
    driver.switch_to.window(window_name=driver.window_handles[0])

#An action chain to tab down to select public library access, enter username and password, click login
ActionChains(driver)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.ENTER)\
    .send_keys(Keys.ARROW_DOWN)\
    .send_keys(Keys.ARROW_DOWN)\
    .send_keys(Keys.ENTER)\
    .send_keys(Keys.TAB)\
    .send_keys(account)\
    .send_keys(Keys.TAB)\
    .send_keys(password)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.ENTER)\
    .perform()
time.sleep(2)

# Opens OCPLL lexis page and sets bookID, creates a new folder directory to store the book files
driver.get("https://lexisdl.com/library/ocpll/open/" + book_ID)
time.sleep(5)

#if book is not checked out, check it out
if(driver.title !="Open book | LexisNexis Digital Library" and driver.title != "Login | LexisNexis Digital Library"):
    driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[1]/main/div/div/section/div[2]/button').click()
    ActionChains(driver)\
        .send_keys(Keys.TAB)\
        .send_keys(Keys.ENTER)\
        .perform()

#in the e-reader, iterate through sections in table of contents, print each section; the first time we need to check that the navigation informaiton has "loaded"
time.sleep(10)
sectionnumber = 0

#ensures we are on the first section and navigation information is loaded
ActionChains(driver)\
    .key_down(Keys.SHIFT)\
    .send_keys("n")\
    .key_up(Keys.SHIFT)\
    .perform()
time.sleep(3)
#load navigation data
ActionChains(driver)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.ENTER)\
    .perform()
time.sleep(30)
#navigate to first section
ActionChains(driver)\
    .key_down(Keys.SHIFT)\
    .send_keys("c")\
    .key_up(Keys.SHIFT)\
    .perform()
time.sleep(1)
ActionChains(driver)\
    .send_keys(Keys.TAB)\
    .perform()
time.sleep(1)
ActionChains(driver)\
    .send_keys(Keys.TAB)\
    .perform()
time.sleep(1)
ActionChains(driver)\
    .send_keys(Keys.TAB)\
    .perform()
time.sleep(1)
ActionChains(driver)\
    .send_keys(Keys.TAB)\
    .send_keys(Keys.ENTER)\
    .perform()
time.sleep(3)

#prints each section while last two files are not equal
file2 = "2"
file1 = "1"
iteration = 0

while (iteration < 2 or not (os.path.getsize(file1)==os.path.getsize(file2))):
    #Saves/prints as pdf current section
    ActionChains(driver)\
        .key_down(Keys.COMMAND)\
        .send_keys("p")\
        .key_up(Keys.COMMAND)\
        .perform()
    time.sleep(5)
    #Navigates to next section
    ActionChains(driver)\
        .key_down(Keys.SHIFT)\
        .send_keys("n")\
        .send_keys(Keys.ARROW_RIGHT)\
        .key_up(Keys.SHIFT)\
        .perform()
    time.sleep(5)
    #update files for comparison
    list_of_files = list(filter(os.path.isfile, glob.glob(directory + "/" + "*")))
    list_of_files.sort(key=lambda x: os.path.getmtime(x))
    file1 = list_of_files[-1]
    if iteration > 0:
        file2 = list_of_files[-2]
    print("iteration: " + str(iteration) + "file1: " + str(file1) + "file2: " + str(file2))
    iteration += 1
