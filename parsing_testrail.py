from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


#opening test-run and login
def login(test_run, email, password, driver):
    driver.get(test_run)
    driver.maximize_window()
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, 'name')))
    element = driver.find_element_by_id("name")
    element.send_keys(email)
    element = driver.find_element_by_id("password")
    element.send_keys(password)
    element.send_keys(Keys.RETURN)


#select need sort
def sorting(driver):
    time.sleep(1)
    try:
        driver.find_element_by_id('orderByReset').click()
    except:
        pass
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="orderByChange"]')))
    driver.find_element_by_xpath('//*[@id="orderByChange"]').click()
    driver.find_element_by_xpath('//*[@id="orderDropdown"]/ul/li[20]').click()
    time.sleep(1)


#select need filter
def filter(driver, only_today):
    try:
        driver.find_element_by_id('filterByReset').click()
        time.sleep(1)
    except:
        pass
    if only_today:
        driver.find_element_by_xpath('//*[@id="filterByChange"]').click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="filter-tests:tested_on"]/div[1]/a[1]')))
        driver.find_element_by_xpath('//*[@id="filter-tests:tested_on"]/div[1]/a[1]').click()
        driver.find_element_by_xpath('//*[@id="filterTestsApply"]').click()
        time.sleep(1)


def time_translation(all_times):
    final_time = 0
    for i in all_times:
        if i == '': continue
        times = i.split(' ')
        for time in times:
            s = time[-1]
            time = time[:-1]
            if s == 'm':
                final_time = final_time + int(time) * 60
            elif s == 's':
                final_time = final_time + int(time)
            elif s == 'h':
                final_time = final_time + int(time) * 3600

    # print(final_time)
    return final_time




#collection and parsing  all data
def parsing(driver):
    estimates = []
    elapseds = []
    result = {}

# Finds what position it is in Elapsed
    header = driver.find_element_by_class_name('header').find_elements_by_xpath('th')
    # print(header)
    for i in header:
        # print(i.text)
        if i.text == 'Elapsed':
            Elapsed_position = header.index(i) + 1
            break
        elif i == header[-1]:
            print('----------------------------------------------------------------')
            print("Error: The Elapsed column was not added to testrail")
            print('----------------------------------------------------------------')
            exit()
    # print(Elapsed_position)

    elements = driver.find_elements_by_class_name("jstree-closed")
    for i in elements:
        i.find_element_by_xpath('a/ins').click()
        who = i.text
        if who == "   Unassigned": continue
        who = who[13:]
        # print(who)
        time.sleep(1)
        how_many = driver.find_elements_by_class_name('text-secondary')[4].text

#collecting time and other values
        all_line = driver.find_element_by_class_name('selectable').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
        all_line.pop(0)
        # print(all_line)
        for line in all_line:
            try:
                # estimates.append(line.find_element_by_xpath('td[7]').text)
                elapseds.append(line.find_element_by_xpath('td[%d]' % Elapsed_position).text)
            except:
                print('херь')
                pass
        # print(elapseds)
        common_elapsed = time_translation(elapseds)
        elapseds.clear()
        # common_estimate = time_translation(estimates)


        result[who] = [int(how_many), common_elapsed]

        # result[who] = [int(how_many), common_estimate, common_elapsed]

        print(result)
    return result



def main(test_run, email, password, path_to_chrome_driver, only_today):
    print('Parsing_testrail started work')
    driver = webdriver.Chrome(path_to_chrome_driver)
    login(test_run, email, password, driver)
    sorting(driver)
    filter(driver, only_today)
    result = parsing(driver)
    print('Parsing_testrail finishes work successfully')
    return result

