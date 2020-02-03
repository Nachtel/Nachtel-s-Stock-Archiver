from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os
import time

class stock_history:
    def __init__(self, name, date, close, change, changepercent, opxn, high, low, volume):
        self.name = name
        self.date = date
        self.close = close
        self.change = change
        self.changepercent = changepercent
        self.opxn = opxn
        self.high = high
        self.low = low
        self.volume = volume
        


#driver = webdriver.Firefox()
#driver.get("https://investorshub.advfn.com/secure/login.aspx")

#username = driver.find_element_by_xpath('//*[@id="ctl00_CP1_LoginView1_Login1_UserName"]')
#username.send_keys('Stock_Archiver')

#password = driver.find_element_by_xpath('//*[@id="ctl00_CP1_LoginView1_Login1_Password"]')
#password.send_keys('mood')
#password.send_keys(Keys.ENTER)
#time.sleep(5)
#driver.get("https://www.advfn.com/nyse/newyorkstockexchange.asp?companies=A")


#First item of each table of each page always has the value 3, so the default value of l_num is 3. After all info is recorded from a listing, l_num increases by 1, and thus continues on to the next listing; if the next number is a blank inbetween, then it simply increases l_num again until it finds the next listing. If it reports the same NoSuchElementException 4 times, then the program assumes there are no more listings, and decides
row_dict = {}
def scan(cycles=None):
    page_num = 1
    l_num = 3
    error_counter = 0
    row_num = 2
    default_historical = 4
    #row_dict = {}

    driver = webdriver.Firefox()
    driver.get("https://investorshub.advfn.com/secure/login.aspx")
    
    username = driver.find_element_by_xpath('//*[@id="ctl00_CP1_LoginView1_Login1_UserName"]')
    username.send_keys('Stock_Archiver')

    password = driver.find_element_by_xpath('//*[@id="ctl00_CP1_LoginView1_Login1_Password"]')
    password.send_keys('mood')
    password.send_keys(Keys.ENTER)

    time.sleep(5)

    driver.get("https://www.advfn.com/nyse/newyorkstockexchange.asp?companies=A")
    if cycles is not None:
        for cycle in range(cycles):
            try:
                page = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/div/a[{}]".format(page_num))
                page.click()

                listing = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr[{}]/td[1]/a".format(l_num))
                listing.click()
                listing_name = driver.find_element_by_xpath("/html/body/div[9]/div[5]/div[1]/div/div[1]/h1/strong").text
                #history = driver.find_element_by_name("Historical Data for AKS")a
                while True:
                    history = driver.find_element_by_xpath("/html/body/div[6]/ul/li[{}]/a".format(default_historical))
                    history.click()
                    time.sleep(2)
                    try:
                        #testing to see if element is in the page; if not then the element at the XPATH is not the history data and will be fixed accordingly.
                        testelement = driver.find_element_by_xpath("/html/body/div[9]/div[4]/div[2]/div[1]/div[1]/div/div[2]/table/tbody/tr[2]/td[2]/b")
                        default_historical = 4
                        break
                    except NoSuchElementException:
                    
                        if default_historical <=  9:

                            print("Cannot find the Historical tab in specified area; trying again in next")
                            default_historical += 1
                            driver.back()
                        
                        else:
                            print("3 tries are over...")
                            break

                morehistory = driver.find_element_by_xpath("/html/body/div[7]/ul/li[3]/a")
                morehistory.click()
                time.sleep(2)
                while True:
                    try:
                        for column in range(1, 9):
                            print("Row {}, column value {} read.".format(row_num, column))
                            history_data = driver.find_element_by_xpath("/html/body/div[9]/div[4]/div[2]/div[1]/div[2]/table/tbody/tr[{}]/td[{}]".format(row_num, column))
                            if column == 1:
                                r_date = history_data.text
                            elif column == 2:
                                r_close = history_data.text
                            elif column == 3:
                                r_change = history_data.text
                            elif column == 4:
                                r_changepercent = history_data.text
                            elif column == 5:
                                r_opxn = history_data.text
                            elif column == 6:
                                r_high = history_data.text
                            elif column == 7:
                                r_low = history_data.text
                            elif column == 8:
                                r_volume = history_data.text
                        print("------------------------------")
                        row_dict["{}, row_{}".format(listing_name, row_num)] = stock_history(listing_name, r_date, r_close, r_change, r_changepercent, r_opxn, r_high, r_low, r_volume)
                        row_num +=1
                    except NoSuchElementException:
                        print("There is no data for this stock")
                        break


                    if row_num > 31:
                        row_num = 2
                        break
    
                driver.get("https://www.advfn.com/nyse/newyorkstockexchange.asp?companies=A")
                l_num +=1
                print("Scanning Page {}, Listing {}...".format(page_num, l_num))

                if error_counter > 0:
                    print("Error corrected; turning error counter back by 1...")
                    error_counter -= 1
            
            except NoSuchElementException:
            
                if error_counter < 4:

                    l_num +=1
                    error_counter +=1
                
                    print("This attempt failed, error counter is now {}; trying again under the next available listing...".format(error_counter))
            
                elif page_num > 27:
                    break

                else:
                    print("Page scanned; moving on to next page...")
                    l_num = 3
                    error_counter = 0
                    page_num +=1
    else:
        while True:
            try:
                page = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/div/a[{}]".format(page_num))
                page.click()

                listing = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr[{}]/td[1]/a".format(l_num))
                listing.click()
                listing_name = driver.find_element_by_xpath("/html/body/div[9]/div[5]/div[1]/div/div[1]/h1/strong").text
                #history = driver.find_element_by_name("Historical Data for AKS")a
                while True:
                    history = driver.find_element_by_xpath("/html/body/div[6]/ul/li[{}]/a".format(default_historical))
                    history.click()
                    time.sleep(2)
                    try:
                        #testing to see if element is in the page; if not then the element at the XPATH is not the history data and will be fixed accordingly.
                        testelement = driver.find_element_by_xpath("/html/body/div[9]/div[4]/div[2]/div[1]/div[1]/div/div[2]/table/tbody/tr[2]/td[2]/b")
                        default_historical = 4
                        break
                    except NoSuchElementException:
                    
                        if default_historical <=  9:

                            print("Cannot find the Historical tab in specified area; trying again in next")
                            default_historical += 1
                            driver.back()
                        
                        else:
                            print("3 tries are over...")
                            break

                morehistory = driver.find_element_by_xpath("/html/body/div[7]/ul/li[3]/a")
                morehistory.click()
                time.sleep(2)
                while True:
                    try:
                        for column in range(1, 9):
                            print("Row {}, column value {} read.".format(row_num, column))
                            history_data = driver.find_element_by_xpath("/html/body/div[9]/div[4]/div[2]/div[1]/div[2]/table/tbody/tr[{}]/td[{}]".format(row_num, column))
                            if column == 1:
                                r_date = history_data.text
                            elif column == 2:
                                r_close = history_data.text
                            elif column == 3:
                                r_change = history_data.text
                            elif column == 4:
                                r_changepercent = history_data.text
                            elif column == 5:
                                r_opxn = history_data.text
                            elif column == 6:
                                r_high = history_data.text
                            elif column == 7:
                                r_low = history_data.text
                            elif column == 8:
                                r_volume = history_data.text
                        print("------------------------------")
                        row_dict["{}, row_{}".format(listing_name, row_num)] = stock_history(listing_name, r_date, r_close, r_change, r_changepercent, r_opxn, r_high, r_low, r_volume)
                        row_num +=1
                        return listing, row_num
                    except NoSuchElementException:
                        print("There is no data for this stock")
                        break


                    if row_num > 31:
                        row_num = 2
                        break
    
                driver.get("https://www.advfn.com/nyse/newyorkstockexchange.asp?companies=A")
                l_num +=1
                print("Scanning Page {}, Listing {}...".format(page_num, l_num))

                if error_counter > 0:
                    print("Error corrected; turning error counter back by 1...")
                    error_counter -= 1
            
            except NoSuchElementException:
            
                if error_counter < 4:

                    l_num +=1
                    error_counter +=1
                
                    print("This attempt failed, error counter is now {}; trying again under the next available listing...".format(error_counter))
            
                elif page_num > 27:
                    break

                else:
                    print("Page scanned; moving on to next page...")
                    l_num = 3
                    error_counter = 0
                    page_num +=1

listing_name, row_num = scan
