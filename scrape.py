from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm
import re
from selenium.webdriver.support.ui import WebDriverWait

service = Service("/usr/bin/geckodriver")

options = Options()
options.binary_location = "/usr/bin/firefox" 
options.add_argument("--incognito")
options.set_preference("browser.tabs.remote.autostart", False)
options.set_preference("browser.tabs.remote.autostart.2", False)
options.set_preference("devtools.debugger.remote-enabled", True)
options.set_preference("devtools.debugger.remote-port", 9222)
profile_path = "/home/alvis/.mozilla/firefox/8d6vdn6m.default-release"
profile = FirefoxProfile(profile_path)
options.profile = profile
driver = webdriver.Firefox(service=service, options=options)
dataset = open("dataset.csv", 'w')
dataset.write("Emri,Siperfaqe Totale,Siperfaqe e Brendshme,Dhoma Gjumi,Kati,Statusi,Lloji,Mobiluar,Shikime,Hipoteka,Gjendja,Qera,Cmimi,Zona,Qyteti,Url\n")



def clean_html(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace(u'\xa0', ' ')
    text = ' '.join(text.strip().split())
    return text



with open('urls.txt', 'r') as file:
    urls = [url.strip() for url in file if url.strip() != ""] 


for url in tqdm(urls, desc="Processing URLs"):
    if url != "":
        url = url.strip()
        driver.get(url)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        emri = driver.find_element(By.XPATH, "/html/body/section/div[1]/div[3]/h1").get_attribute("innerHTML").replace(",", ".").strip()
        qera = "jo"
        zona = ""
        qyteti = ""
        full_location = driver.find_element(By.XPATH, "/html/body/section/div[1]/div[1]/div[1]/div[1]/h6").get_attribute("innerHTML").replace("Albania", "").strip()
        if " " in full_location:
            qyteti = full_location.split(" ")[-1].replace(",", ".").strip()
            zona = ' '.join(full_location.split(" ")[:-1]).replace(",", ".").strip()
        else:
            qyteti = full_location
        cmimi = clean_html(driver.find_element(By.XPATH, "/html/body/section/div[1]/div[3]/h2").get_attribute("innerHTML").replace("€","").replace(",", "")).strip()
        if "/Muaj" in cmimi:
            cmimi = cmimi.replace("/Muaj", "").strip()
            qera = "po"
        props = driver.find_elements(By.XPATH, "/html/body/section/div[1]/div[4]/div/div")
        all_props = {
            'emri': emri,
            'siperfaqe_totale': '',
            'siperfaqe_brendshme': '',
            'dhoma_gjumi': '',
            'kati': '',
            'statusi': '',
            'lloji': '',
            'mobiluar': '',
            'shikime': '',
            'hipoteke': '',
            'gjendja': ''
        }
        
    
        for prop in props:
            try:
                p = prop.find_element(By.CLASS_NAME, "paragraph-2")
                text = p.text.strip()
                if text.startswith("Sip. Totale"):
                    key = "siperfaqe_totale"
                    value_span = p.find_element(By.TAG_NAME, "span")
                    value = value_span.text.strip().replace("m2", "")
                    all_props[key] = value
                elif text.startswith("Sip. e brendshme"):
                    key = "siperfaqe_brendshme"
                    value_span = p.find_element(By.TAG_NAME, "span")
                    value = value_span.text.strip().replace("m2", "")
                    all_props[key] = value
                    
                elif text.startswith("Dhomat e gjumit"):
                    key = "dhoma_gjumi"
                    value_span = p.find_element(By.TAG_NAME, "span")
                    value = value_span.text.strip()
                    all_props[key] = value
                elif text.startswith("Kati"):
                    key = "kati"
                    value_span = p.find_element(By.TAG_NAME, "span")
                    value = value_span.text.strip()
                    all_props[key] = value
                elif text.startswith("Statusi"):
                    key = "statusi"
                    value_span = p.find_element(By.TAG_NAME, "span")
                    value = value_span.text.strip()
                    all_props[key] = value
                elif text.startswith("Lloji"):
                    key = "lloji"
                    value_span = p.find_element(By.TAG_NAME, "span")
                    value = value_span.text.strip()
                    all_props[key] = value
                elif text.startswith("Ka hipoteke:"):
                    key = "hipoteke"
                    value = text.split(":")[-1].strip()
                    all_props[key] = value
                elif text.startswith("Shikime:"):
                    key = "shikime"
                    value = text.split(":")[-1].strip()
                    all_props[key] = value
                else:
                    try:
                        svg = prop.find_element(By.TAG_NAME, "svg")
                        use = svg.find_element(By.TAG_NAME, "use")
                        icon_ref = use.get_attribute("xlink:href")

                        if icon_ref == "#furnished-icon":
                            all_props["mobiluar"] = text
                        elif icon_ref == "#status-icon":
                            all_props["gjendja"] = text
                    except:
                        pass
            except:
                continue
        line = ""
        for v in all_props.values():
            line += f"{v.replace(",", ".")},"
        line += f"{qera},{cmimi},{zona},{qyteti},{url}\n"
        dataset = open("dataset.csv", 'a')
        dataset.write(line)
        dataset.close()
        
            

driver.close()