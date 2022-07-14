from pydoc import classname
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from datetime import datetime, date
import calendar
import sys



markets  = [
        {
                "salesChannelId": 1,
                "salesChannelName": "Platform-BE",
                "excludeCategories": [ 3029 ]
        },
        {
                "salesChannelId": 2,
                "salesChannelName": "Platform-CH",
                "excludeCategories": [ 388 ]
        },
        {
                "salesChannelId": 3,
                "salesChannelName": "Platform-DK",
                "excludeCategories": [ 2743 ]
        },
        {
                "salesChannelId": 4,
                "salesChannelName": "Platform-NL",
                "excludeCategories": [ 3047 ]
        },
        {
                "salesChannelId": 5,
                "salesChannelName": "Platform-NO",
                "excludeCategories": [ 2651 ]
        },
        {
                "salesChannelId": 6,
                "salesChannelName": "Platform-PL",
                "excludeCategories": [ 3201 ]
        },
        {
                "salesChannelId": 7,
                "salesChannelName": "Platform-SE",
                "excludeCategories": [ 2414 ]
        },
        {
                "salesChannelId": 8,
                "salesChannelName": "Platform-DE",
                "excludeCategories": [ 428 ]
        },
        {
                "salesChannelId": 9,
                "salesChannelName": "Platform-ES",
                "excludeCategories": [ 433 ]
        },
        {
                "salesChannelId": 10,
                "salesChannelName": "Platform-FI",
                "excludeCategories": [ 428 ]
        },
        {
                "salesChannelId": 11,
                "salesChannelName": "Platform-FR",
                "excludeCategories": [ 429 ]
        },
        {
                "salesChannelId": 12,
                "salesChannelName": "Platform-IT",
                "excludeCategories": [ 430 ]
        },
        {
                "salesChannelId": 13,
                "salesChannelName": "Platform-UK",
                "excludeCategories": [ 428 ]
        }
]


def FindByElementTextContains(driver, text):
    xpath = "//*[contains(text(),'" + text + "')]"
    return driver.find_element(By.XPATH, xpath)

def SetElementValue(driver: webdriver.Remote, element, value):
    driver.execute_script("arguments[0].value='"+ value +"';", element)
    driver.execute_script("arguments[0].blur();", element)

def signin(driver, username, password):

    driver.get("https://proxy-voucher.miinto.net/auth/login")
    assert "Voucher service" in driver.title

    elem = driver.find_element(By.NAME, "username")
    elem.send_keys(username)

    elem = driver.find_element(By.NAME, "password")
    elem.send_keys(password)

    elem = FindByElementTextContains(driver, "Login")
    elem.click()


def createVoucherForMarket(driver: webdriver.Remote, market, voucherName, discountPct, startDate, endDate):
    logLineToBrowser(driver, f"{voucherName}, {discountPct}%")
    

    jsonPayload =  {
        "voucherCode": voucherName,
        "voucherMethod": "percentage",
        "voucherRefundable": False,
        "voucherSalesChannelId": market['salesChannelId'],
        "voucherUsageType": "multiple",
        "voucherValue": discountPct,
        "voucherType": "single",
        "rules": [
            {
                "ruleType": 1,
                "ruleValue": {
                    "date": startDate.strftime("%Y-%m-%dT00:00:00")
                }
            },
            {
                "ruleType": 2,
                "ruleValue": {
                    "date": endDate.strftime("%Y-%m-%dT23:59:59")
                }
            },
            {
                
                "ruleType": 5,
                "ruleValue": {
                    "include": False,
                    "categories": market['excludeCategories']
                }
            }
        ]
    }

    cookies = driver.get_cookies()
    sessionId = [c for c in cookies if c["name"] == 'PHPSESSID'][0]["value"]

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Cookie": f"PHPSESSID={sessionId}"
        }



    res = requests.post("https://proxy-voucher.miinto.net/vouchers", headers=headers, json = jsonPayload)
    
    logLineToBrowser(driver, "Success", "success")

    if res.status_code != 200:
            logLineToBrowser("Failed!!", "error")


def prepareLoggingCanvas(driver: webdriver.Remote):
    script = f"""
        document.getElementsByTagName("body")[0].remove();
        var body = document.createElement("body");
        var html = document.getElementsByTagName("html")[0];
        var head = document.createElement("head");
        head.innerHTML = '<style>.log-line {{  }} .success {{ color: green; }} .error {{ color: red; }} .strong {{ font-weight: bold; }} .large1 {{ font-size: 30px; }} .large2 {{ font-size: 20px; }}</style>'
        html.appendChild(head)
        html.appendChild(body);
        
    """
    driver.execute_script(script)

def logLineToBrowser(driver: webdriver.Remote, message, className = 'regular'):

    script = f"""
        var root = document.getElementsByTagName("body")[0]
        var p = document.createElement("p");
        p.classList.add('log-line', '{className}');
        var text = document.createTextNode("{message}");
        p.appendChild(text)
        root.appendChild(p);
    """
    driver.execute_script(script)

def logTextToBrowser(driver: webdriver.Remote, message):

    script = f"""
        var root = document.getElementsByTagName("body")[0]
        var text = document.createTextNode("{message}");
        root.appendChild(text);
    """
    driver.execute_script(script)

def waitForDashboard(driver):
    print("Waiting to reach dashboard - please sign in!")
    WebDriverWait(driver, 5000).until(
        EC.url_contains("/dashboard")
    )
    print("Voucher dashboard reached")


def initializeWebDriver():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(30)
    driver.start_client
    return driver

def getPrefixArg():
    return sys.argv[1]

def getDateArg():
    return sys.argv[2]

def run():

    prefix = getPrefixArg()
    startdate = getDateArg()

    startDate = datetime.strptime(startdate, '%d-%m-%Y')
    endDate = date(startDate.year, startDate.month, calendar.monthrange(startDate.year, startDate.month)[1])

    driver = initializeWebDriver()
    signin(driver, "<username>", "<password>")

    waitForDashboard(driver)
    prepareLoggingCanvas(driver)
    logLineToBrowser(driver, "Logged in successfully", "large1")  
    logLineToBrowser(driver, f"Will create vouchers from {startDate} to {endDate}")
    
    for m in markets:
        input(f"Pres enter to create: {m['salesChannelName']}")
        logLineToBrowser(driver, f".")
        logLineToBrowser(driver, f"{m['salesChannelName']}", "large2")
        createVoucherForMarket(driver, m, f"Friends&Family{prefix}", 20, startDate, endDate)
        createVoucherForMarket(driver, m, f"MiintoEmployee{prefix}", 25, startDate, endDate)

    inp = input('All done. Press enter to exit!')
    driver.close()



if __name__ == "__main__":
    run()