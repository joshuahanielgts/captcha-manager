import os
import time
import re
import getpass
import logging
from PIL import Image
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Path to Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Securely get credentials
net_id = input("Enter SRM Net ID: ")
passwd = getpass.getpass("Enter Password: ")

# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        driver.get("https://sp.srmist.edu.in/srmiststudentportal/students/loginManager/youLogin.jsp")
        wait = WebDriverWait(driver, 10)

        username = wait.until(EC.presence_of_element_located((By.ID, "login")))
        password = wait.until(EC.presence_of_element_located((By.ID, "passwd")))
        captcha_img = wait.until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'captcha')]")))
        captcha_img.screenshot("captcha.png")

        try:
            img = Image.open("captcha.png").convert('L')
            img = img.resize((img.width * 2, img.height * 2))  # Upscale for better OCR
            img = img.point(lambda x: 0 if x < 140 else 255)
            captcha_text = pytesseract.image_to_string(img, config='--psm 7').strip()
            captcha_text = re.sub(r'\W+', '', captcha_text)
            logging.info(f"Captcha OCR: {captcha_text}")
        except Exception as e:
            logging.warning(f"OCR failed: {e}")
            img.show()
            captcha_text = input("Enter captcha manually: ")

        username.clear()
        time.sleep(2)
        username.send_keys(net_id)
        password.clear()
        time.sleep(2)
        password.send_keys(passwd)

        captcha_field = wait.until(EC.presence_of_element_located((By.NAME, "ccode")))
        captcha_field.clear()
        time.sleep(2)
        captcha_field.send_keys(captcha_text)

        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button']")))
        time.sleep(1)
        login_button.click()

        time.sleep(3)

        error_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Captcha')]")
        if error_elements:
            logging.warning("Wrong captcha. Retrying...")
            attempts += 1
            continue

        logging.info("Captcha accepted. Assuming login succeeded.")
        print("You're inside.")
        input("Press Enter when you're done and want to logout and close the browser...")
        break

    else:
        logging.error("Too many captcha failures. Try again manually.")

finally:
    if os.path.exists("captcha.png"):
        os.remove("captcha.png")
    try:
        driver.get("https://sp.srmist.edu.in/srmiststudentportal/students/template/Logout.jsp")
        time.sleep(2)
    except:
        pass
    driver.quit()
