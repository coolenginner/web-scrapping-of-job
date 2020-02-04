import csv
import os
import time
from datetime import datetime
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains

class WebTable:
    def __init__(self, webtable):
       self.table = webtable
       
    def row_data(self, row_number):
        if(row_number == 0):
            raise Exception("Row number starts from 1")

        row_number = row_number + 1
        row = self.table.find_elements_by_xpath("//tr["+str(row_number)+"]/td")
        rData = []
        for webElement in row :
            rData.append(webElement.text)

        return rData

if __name__ == "__main__":
    
    binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
    caps = DesiredCapabilities().FIREFOX
    caps["marionette"] = True
    driver = webdriver.Firefox(capabilities=caps, firefox_binary=binary, executable_path="geckodriver.exe")
    driver.get("http://offstagejobs.com/jobs.php")
  
    print("Starting...")

    try:
        driver.find_element_by_xpath("//select[@name='page']/option[text()='Display All']").click()
        time.sleep(1)
    except NoSuchElementException:
        print('Something is not right.')

    try:
        search_button = driver.find_element_by_xpath(
            '//input[contains(@name, "query_check")]')
        ActionChains(driver).move_to_element(search_button).click().perform()
        time.sleep(15)
    except NoSuchElementException:
        print('Something is not right.')

    print("Scraping...")

    final_data = []
    html = driver.page_source
    parsed_html = BeautifulSoup(html, features="html.parser")

    data1 = parsed_html.find_all('div', attrs={'class':'itemh1'})
    data2 = parsed_html.find_all('div', attrs={'class':'itemh2'})
    data3 = parsed_html.find_all('div', attrs={'class':'itemContact'})
    data4 = parsed_html.find_all('span', attrs={'class':'emu'})

    i = 0
    for j in data2:
        dataitem = list()
        temp = list()
        print(i)

        try: 
            temp = data1[i + 1].text.splitlines()
            dataitem.append(temp[1])
            print(temp[1])
        except IndexError: 
            dataitem.append("")

        try:
            temp = data2[i].text.splitlines()
            dataitem.append(temp[1].strip())
            print(temp[1].strip())
        except IndexError: 
            dataitem.append("")

        try:
            temp = data3[i].text.splitlines()
            dataitem.append(temp[2])
            print(temp[2])
        except IndexError:
            dataitem.append("")

        try:
            temp = data4[i].text.splitlines()
            dataitem.append(temp[0])
            print(temp[0])
        except IndexError:
            dataitem.append("")

        final_data.append(dataitem)
        i = i + 1
    
    final_data.insert(0, ['Job Title', 'Company', 'Name', 'Email'])

    now = datetime.now()
    name = now.strftime("%m%d%Y%H%M%S")
    fileName = name + ".csv"

    with open(fileName, 'w',newline='') as fp:
        a = csv.writer(fp, delimiter =',')
        a.writerows(final_data)
    print("Done.")
    