from selenium.common import ElementNotInteractableException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import google.generativeai as genai
import time
import os
from dotenv import load_dotenv
load_dotenv()

key = os.environ.get('API_KEY')
print(key)


def gemini(question):
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[])
    response = chat.send_message(question + " provide only the selected option letter and a period (e.g., 'c. '")
    time.sleep(8)
    answer = response.text
    return answer


def process(driver):
    links = [] #array of quiz links

    for i in links:
        # quiz_url = input("Enter the Url for the MCQ: ")
        quiz_url = i
        driver.get(quiz_url)

        try:
            driver.find_element(By.XPATH, "//button[text()='" + "Attempt quiz" + "']").click()
        except:
            try:
                driver.find_element(By.XPATH, "//button[text()='" + "Continue your attempt" + "']").click()
            except:
                driver.find_element(By.XPATH, "//button[text()='" + "Re-attempt quiz" + "']").click()
        while True:
            time.sleep(5)
            question = driver.find_element(By.CLASS_NAME, "qtext").text
            option = driver.find_element(By.CLASS_NAME, "answer").text
            print(option)

            try:
                ans = gemini(question + option)
                ans = ans[0:3].lower()
            except Exception as err:
                print(err)
                print("Retrying in 20 Seconds...")
                time.sleep(20)
                ans = gemini(question + option)
                ans = ans[0:3]

            print(ans, len(ans))
            try:
                try:
                    driver.find_element(By.XPATH, "//span[text()='" + ans.lower() + "']").click()
                except:
                    driver.find_element(By.XPATH, "//span[text()='" + ans.upper() + "']").click()
            except:
                try:
                    driver.find_element(By.XPATH, f"//label[contains(text(), '{ans.lower()}')]").click()
                    time.sleep(1)
                except:
                    driver.find_element(By.XPATH, f"//label[contains(text(), '{ans.upper()}')]").click()
                    time.sleep(1)
            try:
                driver.find_element(By.XPATH, '//input[@value="Next page"]').click()
            except:
                driver.find_element(By.XPATH, '//input[@value="Finish attempt ..."]').click()
                time.sleep(5)
                driver.find_element(By.XPATH, "//button[text()='" + "Submit all and finish" + "']").click()
                time.sleep(5)

                try:
                    modal = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='modal-content']")))
                    modal = WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.XPATH, "//div[@class='modal-content']")))

                    submit_button = modal.find_element(By.XPATH, "//button[@data-action='save']")
                    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                    WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@data-action='save']")))

                    try:
                        submit_button.click()
                    except (ElementNotInteractableException, ElementClickInterceptedException):
                        print("Element is not interactable or click intercepted. Trying alternative click.")
                        driver.execute_script("arguments[0].click();", submit_button)

                except TimeoutException:
                    print("Modal did not appear in time")

                break
