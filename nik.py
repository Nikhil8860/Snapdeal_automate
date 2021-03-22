from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import os
from time import sleep

directory = 'downloads'

if os.path.exists(directory):
    import shutil
    shutil.rmtree(directory)
else:
    pass

os.mkdir(directory)
cw = os.getcwd()
t = os.path.join(cw, directory)


chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : t}
chromeOptions.add_experimental_option("prefs",prefs)
# chromeOptions.add_argument("--user-data-dir=chrome-data")

browser = webdriver.Chrome(executable_path=r"C:\Users\nikhils3\Desktop\chromedriver.exe", options=chromeOptions)
action = ActionChains(browser)
browser.get(r'https://seller.flipkart.com/sell-online/')
browser.find_element_by_class_name('sc-qamJO').click()
browser.find_element_by_name('username').send_keys('ankurvaghasiya76@gmail.com')
browser.find_element_by_name('password').send_keys('HAPPYankur123#')
browser.find_element_by_class_name('jqsSXx').click()
sleep(5)
element_to_hover_over = browser.find_element_by_xpath('//*[@id="Orders"]/a')

hover = ActionChains(browser).move_to_element(element_to_hover_over)
hover.perform()
sleep(5)
browser.find_element_by_xpath('//*[@id="Orders"]/ul/li[3]/a').click()
sleep(5)

print('hello')

