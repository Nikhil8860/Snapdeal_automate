from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PyPDF2 import PdfFileMerger, PdfFileReader
import os
from tika import parser
import re
from pathlib import Path
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
from PIL import Image
from pdf2image import convert_from_path
from pdf2image.exceptions import (PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError)
from PyPDF2 import PdfFileWriter as w


directory = f'downloads_{datetime.datetime.today().date()}_{datetime.datetime.now().date()}'

os.mkdir(directory)
cw = os.getcwd()
t = os.path.join(cw, directory)

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : t}
chromeOptions.add_experimental_option("prefs",prefs)
# chromeOptions.add_argument("--user-data-dir=chrome-data")

# driver = webdriver.Chrome(r'C:\python\chromedriver.exe',options=chrome_options)

browser = webdriver.Chrome(executable_path=r"C:\Users\nikhils3\Desktop\chromedriver.exe", options=chromeOptions)
action = ActionChains(browser)

browser.get(r'https://seller.flipkart.com/sell-online/')
browser.find_element_by_class_name('sc-qamJO').click()
browser.find_element_by_name('username').send_keys('ankurvaghasiya76@gmail.com')
browser.find_element_by_name('password').send_keys('HAPPYankur123#')
browser.find_element_by_class_name('jqsSXx').click()
time.sleep(5)
element_to_hover_over = browser.find_element_by_xpath('//*[@id="Orders"]/a')

hover = ActionChains(browser).move_to_element(element_to_hover_over)
hover.perform()
time.sleep(5)
browser.find_element_by_xpath('//*[@id="Orders"]/ul/li[3]/a').click()

# browser.get(r'https://seller.flipkart.com/index.html#dashboard/fbflite-ff/LOC170aa9c0f285489b8d1040cc2f672012/nav-ff/new')

browser.find_elements_by_class_name('reports-dropdown-picklist-text').click()
browser.find_element_by_class_name('generate-regular-picklist').click()

#picklist_pdf processing
files = []
for i in os.listdir('downloads'):
    if i.startswith('Flipkart'):
        files.append(i)

picklist_pdf = files[0]
parsed_pdf = parser.from_file(picklist_pdf)
data = parsed_pdf['content'].split('LID / WID')[1]
PickListId = parsed_pdf['content'].split('LID / WID')[0].split('Pick List')[0].strip()
info = re.findall(r"[A-Z]{7,}\d+\w+", data)
print(info)
print(PickListId.split()[1])
picklist_id = PickListId.split()[1]
lid_wid = info


# select dispatch
browser.find_element_by_xpath('//*[@id="blinx-wrapper-6"]/ul/li[3]/span').click()

#picklist_id entry
browser.find_element_by_class_name('picklistId-input').send_keys(picklist_id)

# lid_wid entry
import time
for i in lid_wid:
    browser.find_element_by_class_name().send_keys(i)
    time.sleep(5)
    # dirpath = 'downloads'
    paths = sorted(Path(directory).iterdir(), key=os.path.getctime)
    order_pdf = paths[-1]
    parsed_pdf = parser.from_file(parsed_pdf)
    data = parsed_pdf['content']
    tracking_id = re.findall('Tracking ID:(\s+\w+)', data)
    trac_id = tracking_id[0].strip()

    browser.find_element_by_class_name().send_keys(trac_id)
    time.sleep(5)

files = []
for i in os.listdir(directory):
    if not i.startswith('Flipkart'):
        files.append(i)
mergedObject = PdfFileMerger()
for fileNumber in files:
    mergedObject.append(PdfFileReader(f'{directory}\\{fileNumber}', 'rb'))

mergedObject.write(f"mergedfile_{datetime.datetime.today()}_{datetime.datetime.now()}.pdf")

merged_files =[]
for ii in os.listdir(directory):
    if ii.startswith('mergedfile_'):
        files.merged_files(ii)

pages = convert_from_path(f'{directory}\\{merged_files[0]}')
count = 0
label_list = []
invoice_list = []
for page in pages:
    count+=1
    im = page
    width, height = im.size

    xcenter = im.width / 2
    ycenter = im.height / 2

    # upper_label processing
    xu1 = xcenter - 341
    yu1 = ycenter - 1086
    xu2 = xcenter + 340
    yu2 = ycenter - 138
    # lower_label processing
    xl1 = xcenter - 720
    yl1 = ycenter - 140
    xl2 = xcenter + 710
    yl2 = ycenter + 720

    iml = im.crop((xu1, yu1, xu2, yu2))
    imi = im.crop((xl1, yl1, xl2, yl2))
    if count == 1:
        imll = iml
        imii = imi
        continue
    label_list.append(iml)
    invoice_list.append(imi)

label=open(f"{directory}//labels.pdf", "wb")
invoice=open(f"{directory}//invoices.pdf", "wb")

imll.save(label, "PDF" ,resolution=100.0, save_all=True, append_images=label_list)
imii.save(invoice, "PDF" ,resolution=100.0, save_all=True, append_images=invoice_list)
label.close()
invoice.close()
