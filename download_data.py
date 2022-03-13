import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from id_pass_ex import ID, PASS

base = os.path.abspath("")
PATH = os.path.join(base, r"cdriver\chromedriver.exe")
URL = "https://www2.order-fulfillment.bz/benzara/pendinginventorynotice/pendinginventorylist"

options = Options()
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")

# default download directory
chrome_prefs = {"download.default_directory": os.path.join(base, "data")}
options.experimental_options["prefs"] = chrome_prefs


def login(url, options):
    print('Process Started...')
    driver = webdriver.Chrome(service=Service(PATH), options=options)
    driver.get(url)
    driver.implicitly_wait(7)
    time.sleep(.3)

    login_id = driver.find_element(By.ID, "LoginId")
    pass_box = driver.find_element(By.ID, "Password")
    time.sleep(.2)
    login_id.send_keys(ID)
    time.sleep(.1)
    pass_box.send_keys(PASS)

    sign_in = driver.find_element(By.ID, "btnLogin")
    time.sleep(.2)
    sign_in.click()
    print("log in complete")

    driver.implicitly_wait(4)
    time.sleep(2)

    log_file = open("log.txt", "a")
    grid_body = driver.find_element(By.CLASS_NAME, "grid-body")
    rows = grid_body.find_elements(By.CLASS_NAME, "row")

    for row in rows:
        time_stamp, p_ip = row.find_elements(By.CLASS_NAME, "col-md-2")
        c_name = row.find_element(By.CLASS_NAME, "col-md-3").text
        print(f"{time_stamp.text}: {c_name} -- {p_ip.text}")
        log_file.write(f"{time_stamp.text}: {c_name} -- {p_ip.text}\n")

        if p_ip.text == "Processed":
            link_div = row.find_element(By.CLASS_NAME, "col-md-5")
            links = link_div.find_elements(By.CLASS_NAME, "underline-link")
            print(f"downloading files for {c_name} -- {time_stamp.text}")
            for link in links:
                link.click()
                time.sleep(1)

    log_file.close()

    return


login(URL, options)
