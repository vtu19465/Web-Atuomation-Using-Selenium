from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pickle
import os
from dotenv import load_dotenv
load_dotenv()

chrome_options = Options()
# chrome_options.add_argument('--headless')

def save_cookies(driver, location):
    with open(location, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookies(driver, location, url=None):
    cookies = pickle.load(open(location, 'rb'))
    driver.delete_all_cookies()
    for cookie in cookies:
        if 'expiry' in cookie:
            del cookie['expiry']
        driver.add_cookie(cookie)
    if url:
        driver.get(url)

def connect():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
    login_url = "https://lms2.ai.saveetha.in/login"
    driver.get(login_url)

    try:
        driver.get("https://lms2.ai.saveetha.in")
        load_cookies(driver, "cookies.pkl")
        driver.get("https://lms2.ai.saveetha.in")
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='My courses']")))
        except:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//h4[text()='Confirm']")))

    except Exception as err:
        print("except hit...")
        print(err)
        try:
            os.remove('cookies.pkl')
        except:
            pass
        driver.get(login_url)
        rno = os.environ.get("R_NO")
        pas = os.environ.get("PASS")
        u_btn = driver.find_element(By.NAME, "username")
        u_btn.send_keys(rno)
        p_btn = driver.find_element(By.NAME, "password")
        p_btn.send_keys(pas)
        time.sleep(4)
        driver.find_element(By.ID, "loginbtn").click()
        time.sleep(10)
        save_cookies(driver, "cookies.pkl")

    return driver

