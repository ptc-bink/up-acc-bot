from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import os
import datetime
from time import sleep
import json

def wait(callback, data):
    cnt = 0 
    flag = True
    while flag:
        try:
            callback()
            flag = False
            # return
        except WebDriverException as e:
            sleep(1)
            print(f"{cnt} : error in {data} : type -->", type(e).__name__)
            cnt += 1
            if cnt == 10: 
                raise Exception("too late")

def select_nations(country):
    with open("country.json") as json_data:
        data = json.load(json_data)
        index = 0
        for i in range(len(data)):
            if data[i] == country:
                index = i
                break

        return index

def get_info(stack):
    info_path = os.path.join(os.getcwd(), "info.json")
    with open(info_path, 'r') as file:
        data = json.load(file)[stack]

    return (
        data['first-name'], 
        data['second-name'],
        data['country'],
        data['password'],
        data['role'],
        data['experience'],
        data['education'],
        data['language'],
        data['skills'],
        data['overview'],
        data['services'],
        data['rate'],
        data['information']
    )

def get_email():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Enable headless mode
    # chrome_options.add_argument('--profile-directory=Profile 16')

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.upwork.com/nx/signup/?dest=home")

    # sleep(3)

    # wait(lambda: driver.find_element(By.By.CSS_SELECTOR, 'button[aria-label="Close"]').click(), "modal close")

    driver.switch_to.new_window("tab")
    driver.get("https://www.lite14.us/10minutemail/")

    account = driver.window_handles[0]
    verify = driver.window_handles[1]

    email = driver.find_element(By.ID, "copymail").get_attribute('value')

    return (driver, account, verify, email)

def init(driver,email,fname,lname,country,password):
    driver.find_elements(By.CLASS_NAME, "up-checkbox-replacement-helper")[1].click()
    driver.find_elements(By.TAG_NAME, "button")[1].click()
    
    driver.find_element(By.ID, "redesigned-input-email").send_keys(email)
    driver.find_element(By.ID, "first-name-input").send_keys(fname)
    driver.find_element(By.ID, "last-name-input").send_keys(lname)
    driver.find_element(By.ID, "country-dropdown").click()
    sleep(2)
    country_number = select_nations(country)
    wait(lambda: driver.execute_script(f'document.querySelectorAll("li.up-menu-item")[{country_number}].click()'), "select country")
    driver.find_element(By.ID, "password-input").send_keys(password)
    wait(lambda: driver.find_elements(By.CLASS_NAME, "up-checkbox-replacement-helper")[1].click(),"checkbox")
    wait(lambda: driver.find_elements(By.CLASS_NAME, "up-checkbox-replacement-helper")[0].click(),"checkbox")
    sleep(1)
    driver.find_element(By.ID, "button-submit-form").click()
    sleep(1)

def get_verify_url(driver):
    cnt = 0
    msg_check = True
    driver.execute_script(f"window.scrollBy(0, 800);")
    while msg_check:
        if cnt == 30:
            raise Exception("too late")
        try:
            driver.find_elements(By.CSS_SELECTOR, "button.collapsible")[0].click()
            verifiedURL = driver.find_elements(By.TAG_NAME, "a")[16].get_attribute('href')
            return verifiedURL
        except : 
            cnt += 1
            sleep(10)

def begin(driver, role):
    wait(lambda: driver.find_element(By.CLASS_NAME, "air3-btn.air3-btn-primary").click(),"get started")
    sleep(2)
    wait(lambda: driver.find_elements(By.CSS_SELECTOR, 'div[data-qa="button-box"]')[2].click(), "i am am expert")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test='next-button']").click(), "next")
    wait(lambda: driver.find_elements(By.CSS_SELECTOR, "div.span-md-3")[0].click(), "earn money")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test='next-button']").click(),"next")
    wait(lambda: driver.find_elements(By.CSS_SELECTOR, "div.d-flex.span-md-4")[0].click(),"check 1")
    wait(lambda: driver.find_elements(By.CSS_SELECTOR, "div.d-flex.span-md-4")[1].click(),"check 2")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, "label[data-test='checkbox-label']").click(),"check 3")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test='next-button']").click(),"next")

    wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-qa='resume-fill-manually-btn']").click(),"fill manually")

    wait(lambda: driver.find_elements(By.CSS_SELECTOR, "input[aria-labelledby='title-label']")[0].send_keys(role),"input role")

    wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test='next-button']").click(),"next")

def add_exp(driver, exp):
    for i in range(len(exp)):
        add = 0
        if i == 0:
            add = 4
        else:
            add = 4
        wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-qa='employment-add-btn']").click(),"add exp btn")

        wait(lambda: driver.find_element(By.CSS_SELECTOR, "input[placeholder='Ex: Software Engineer']").send_keys(''),"select exp title")
        # sleep(1)
        wait(lambda: driver.find_element(By.CSS_SELECTOR, "input[placeholder='Ex: Software Engineer']").send_keys(exp[i]['title']),"input exp title")

        wait(lambda: driver.find_element(By.CSS_SELECTOR, "input[placeholder='Ex: Microsoft']").send_keys(exp[i]['company']),"input company")

        sy, sm = exp[i]['start'].split('.')
        # sleep(1)
        wait(lambda: driver.find_element(By.CSS_SELECTOR, "div[aria-labelledby~='start-date-month']").click(),"click start month")
        sleep(1)
        wait(lambda: driver.execute_script(f'document.querySelectorAll("li.air3-menu-item")[{str(3 + int(sm) - add)}].click()'),"select start month")
        sleep(1)
        wait(lambda: driver.find_element(By.CSS_SELECTOR, "div[aria-labelledby~='start-date-year']").click(),"click start year")
        sleep(1)
        wait(lambda: driver.execute_script(f'document.querySelectorAll("li.air3-menu-item")[{2027 - int(sy) - add}].click()'),"select start year")

        ey, em = exp[i]['end'].split('.')

        sleep(1)
        wait(lambda: driver.find_element(By.CSS_SELECTOR, "div[aria-labelledby~='end-date-month']").click(),"click end year")
        sleep(1)
        wait(lambda: driver.execute_script(f'document.querySelectorAll("li.air3-menu-item")[{str(3 + int(em) - add)}].click()'), 'select end year')
        sleep(1)
        wait(lambda: driver.find_element(By.CSS_SELECTOR, "div[aria-labelledby~='end-date-year']").click(),"click end month")
        sleep(1)
        wait(lambda: driver.execute_script(f'document.querySelectorAll("li.air3-menu-item")[{str(2027 - int(ey) - add)}].click()'),"select end month")
        sleep(1)
        wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-qa='btn-save']").click(), "save exp")
        sleep(1)

    wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test='next-button']").click(), "next to education")

def add_edu(driver, education):
    for i in range(len(education)):
        add = 0
        if i == 0:
            add = 6
        else :
            add = 0
        wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-qa='education-add-btn']").click(), "add education")

        sleep(1)

        wait(lambda: driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Ex: Northwestern University"]').send_keys(education[i]['school']),"input school")

        wait(lambda: driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Ex: Bachelors"]').send_keys(education[i]['degree']),"input degree")
        sleep(0.5)
        wait(lambda: driver.find_element(By.CSS_SELECTOR, 'ul[aria-labelledby="degree-label"]').click(),"select degree")

        wait(lambda: driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Ex: Computer Science"]').send_keys(education[i]['field']),"input field")
        wait(lambda: driver.find_element(By.CSS_SELECTOR, 'ul[aria-labelledby="area-of-study-label"]').click(),"select field")
        
        wait(lambda: driver.find_element(By.CSS_SELECTOR, 'div.air3-dropdown.is-full-width').click(),"open start year")

        wait(lambda: driver.find_elements(By.CSS_SELECTOR, 'li.air3-menu-item')[2026 - int(education[i]['start']) + add].click(),"select start year")

        wait(lambda: driver.find_elements(By.CSS_SELECTOR, 'div.air3-dropdown.is-full-width')[1].click(),"open end year")

        wait(lambda: driver.find_elements(By.CSS_SELECTOR, 'li.air3-menu-item')[2033 - int(education[i]['end']) + add].click(),"select end year")

        wait(lambda: driver.find_element(By.CSS_SELECTOR, 'button[data-qa="btn-save"]').click(),"save btn")

    wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test='next-button']").click(), "next to language")

def add_lang(driver, language):
    lang = ["Basic", "Conversational", "Fluent", "Native or Bilingual"]
    index = lang.index(language)
    wait(lambda: driver.find_element(By.CSS_SELECTOR, 'div[data-test="dropdown-toggle"]').click(), "click language")
    wait(lambda: driver.find_elements(By.CSS_SELECTOR, "li.air3-menu-item")[index].click(), "select language")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test='next-button']").click(), "next to skills")

def add_skills(driver, skills):
    for i in range(len(skills)):
        wait(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="skills-input"]').send_keys(skills[i]),'add skill')
        wait(lambda: driver.find_element(By.CSS_SELECTOR, 'li.is-uncheckable.air3-menu-item').click(),'click skill')

    wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test='next-button']").click(), "next to summary")

def add_summary(driver, overview):
    wait(lambda: driver.find_element(By.CSS_SELECTOR, 'textarea[aria-labelledby="overview-label"]').send_keys(overview), 'input summary')
    wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test='next-button']").click(), "next to category")

def add_servies(driver, services):
    driver.execute_script("document.body.style.zoom='50%'")
    data = []
    service_name = 'services.json'
    service_path = os.path.join(os.getcwd(), service_name)
    with open(service_path, 'r') as file:
        data = json.load(file)
    data_list = []
    for item in services:
        cnt = 0
        for x in data:
            for y in x:
                if y == item:
                    data_list.append([data.index(x), cnt + x.index(y)])
            cnt += len(x)

    wait(lambda: driver.execute_script(f'''document.querySelectorAll('div[data-test="dropdown-toggle"]')[1].click()'''), 'click dropdown service')
    for item in data_list:
        # print(item[0],item[1])
        wait(lambda: driver.execute_script(f'''document.querySelectorAll('li.is-uncheckable.air3-nested-menu-list.air3-multi-select.air3-menu-item')[{item[0]}].click()'''), 'click dropdown service')

        # wait(lambda: driver.find_elements(By.CSS_SELECTOR, 'li.is-uncheckable.air3-nested-menu-list.air3-multi-select.air3-menu-item')[item[0]].click(), 'click service')
        sleep(0.5)
        driver.execute_script(f"window.scrollBy(0, 800);")
        # wait(lambda: driver.find_elements(By.CSS_SELECTOR, 'span.air3-menu-checkbox-label')[item[1]].click(), 'select service')
        wait(lambda: driver.execute_script(f'''document.querySelectorAll('span.air3-menu-checkbox-label')[{item[1]}].click()'''), 'select service')
        sleep(2)
    driver.execute_script("document.body.style.zoom='100%'")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test='next-button']").click(), "next to rate")

def add_rate(driver, rate):
        wait(lambda: driver.find_element(By.CSS_SELECTOR, 'input[data-ev-label="currency_input"]').send_keys(rate), 'input rate')
        wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test='next-button']").click(), "next to final")

def add_info(driver, info):
    wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-qa=\"open-loader\"]").click(), "select avatar")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, "input[type=\"file\"]").send_keys(os.path.join(os.getcwd(), 'avatar.png')), "upload avatar")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, 'button[data-qa="btn-save"]').click(), "attach avatar")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="street-label"]').send_keys(info['street']), "input street")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Apt/Suite"]').send_keys(info['apt']), "input apt")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="city-label"]').send_keys(info['city']), "input city")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, 'li.is-uncheckable.air3-menu-item').click(), "select city")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="postal-code-label"]').send_keys(info['zipcode']), "input zip code")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, 'input[inputmode="numeric"]').send_keys(info['phone']), "input phone nmber")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test='next-button']").click(), "check to profile")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, 'button[data-qa="submit-profile-top-btn"]').click(), "submit profile")
    wait(lambda: driver.find_element(By.CSS_SELECTOR, 'a.up-n-link.air3-btn.air3-btn-secondary').click(), "view profile")

def main(stack):
    fname = ''
    lname = ''
    country = ''
    password = ''
    role = ''
    exp = []
    education = []
    language = ''
    skills = []
    overview = ''
    services = []
    rate = ''
    info = {}

    (fname, lname, country, password, role, exp, education, language, skills, overview, services, rate, info) = get_info(stack)

    (driver, account, verify, email) = get_email()

    driver.switch_to.window(account)

    init(driver,email,fname,lname,country,password)    

    driver.switch_to.window(verify)

    verifiedURL = get_verify_url(driver)

    if verifiedURL is None:
        return
    
    driver.switch_to.window(account)

    driver.get(verifiedURL)

    begin(driver, role)

    add_exp(driver, exp)
    
    add_edu(driver, education)

    add_lang(driver, language)

    add_skills(driver, skills)

    add_summary(driver, overview)

    add_servies(driver, services)
    
    add_rate(driver, rate)

    add_info(driver, info)
    
    file_name = 'email.json'
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)

    if not isinstance(data, list):
        data = []

    data.append(email)

    with open(file_name, 'w') as file:
        json.dump(data, file)

total = 0

with open('email.json', 'w') as file:
        json.dump([], file)

while True :
    try : 
        if total == 20:
            today = datetime.date.today()
            day_month = today.strftime("%m.%d")

            current_filename = 'email.json'
            new_filename = 'email-' + day_month + '.json'

            os.rename(current_filename, new_filename)
            break 
        main("python-AI")
        total = total + 1
    except KeyboardInterrupt as exit: 
        print("< ------------------------ stopped! ------------------------ >")
        break
    except:
        pass
