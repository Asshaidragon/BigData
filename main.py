import parsing_testrail
import write_to_exel
import parsing_txt
from datetime import *
from openpyxl import load_workbook
from selenium import webdriver

time = datetime.now().strftime('%d.%m.%y %H:%M')


# Receiving values from DATA_CURENT_USER.txt
# -----------------------------------------
value = parsing_txt.main()
email = value['Email=']
password = value['Password=']
test_run = value['Test_run=']
path_to_file = value['Path_to_file=']
list_name = value['List_name=']
path_to_chrome_driver = value['Path_to_chrome_driver=']
only_today = True if value['Only_today='] == 'True' else False
# -------------------------------------------


# Call def parsing_testrail
result = parsing_testrail.main(test_run, email, password, path_to_chrome_driver, only_today)

# Writing the result in excel
write_to_exel.exel(time, result, path_to_file, list_name)


# TO DO
