from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


options = Options()
options.add_argument("--incognito")
profile = FirefoxProfile()
options.profile = profile
driver = webdriver.Firefox(options=options)
f = open("urls.txt", "w")

for i in range(1, 843):
    driver.get(f"https://www.century21albania.com/properties?page={str(i)}")
    carts = driver.find_elements(By.XPATH, "/html/body/div[4]/div[2]/div")
    for cart in carts:
        url = cart.find_element(By.XPATH, "./a").get_attribute("href")
        f = open("urls.txt", "a")
        f.write(url + "\n")
        f.close()
driver.close()