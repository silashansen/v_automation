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
                "salesChannelIdentifier": "9a4dca95-6485-4745-a060-a7a900d32ab0",
                "salesChannelName": "Platform-BE",
                "salesChannelCurrency": "EUR",
                "excludeCategories": [ 3029 ]
        },
        {
                "salesChannelId": 2,
                "salesChannelIdentifier": "bfa5a3d0-9174-437c-aaf2-a8c700acdb3d",
                "salesChannelName": "Platform-CH",
                "salesChannelCurrency": "CHF",
                "excludeCategories": [ 388 ]
        },
        {
                "salesChannelId": 3,
                "salesChannelIdentifier": "cb473b1f-540c-406b-b2d1-a5a800dee649",
                "salesChannelName": "Platform-DK",
                "salesChannelCurrency": "DKK",
                "excludeCategories": [ 2743 ]
        },
        {
                "salesChannelId": 4,
                "salesChannelIdentifier": "f0fac18d-17b4-45d7-b7e2-a5a800dfc3f4",
                "salesChannelName": "Platform-NL",
                "salesChannelCurrency": "EUR",
                "excludeCategories": [ 3047 ]
        },
        {
                "salesChannelId": 5,
                "salesChannelIdentifier": "535765db-5437-4eac-b0b5-a5a800df2290",
                "salesChannelName": "Platform-NO",
                "salesChannelCurrency": "NOK",
                "excludeCategories": [ 2651 ]
        },
        {
                "salesChannelId": 6,
                "salesChannelIdentifier": "8f1b4338-be00-4026-9dec-a7c800ffa5cc",
                "salesChannelName": "Platform-PL",
                "salesChannelCurrency": "PLN",
                "excludeCategories": [ 3201 ]
        },
        {
                "salesChannelId": 7,
                "salesChannelIdentifier": "b2c87ec3-2d50-42b7-87b6-a5a800df7e3a",
                "salesChannelName": "Platform-SE",
                "salesChannelCurrency": "SEK",
                "excludeCategories": [ 2414 ]
        },
        {
                "salesChannelId": 8,
                "salesChannelIdentifier": "048073a5-2b9f-492f-ad23-bf38150211c9",
                "salesChannelName": "Platform-DE",
                "salesChannelCurrency": "EUR",
                "excludeCategories": [ 428 ]
        },
        {
                "salesChannelId": 9,
                "salesChannelIdentifier": "7d1ac383-e0e3-4f4f-8280-d16d4b650ebe",
                "salesChannelName": "Platform-ES",
                "salesChannelCurrency": "EUR",
                "excludeCategories": [ 433 ]
        },
        {
                "salesChannelId": 10,
                "salesChannelIdentifier": "f9425cd6-a73d-4437-9c9c-56a8fa9d9f32",
                "salesChannelName": "Platform-FI",
                "salesChannelCurrency": "EUR",
                "excludeCategories": [ 428 ]
        },
        {
                "salesChannelId": 11,
                "salesChannelIdentifier": "44b206a0-8f7b-4e4c-acde-9d3f819105af",
                "salesChannelName": "Platform-FR",
                "salesChannelCurrency": "EUR",
                "excludeCategories": [ 429 ]
        },
        {
                "salesChannelId": 12,
                "salesChannelIdentifier": "54c850bb-6137-4cca-825e-165a7202c255",
                "salesChannelName": "Platform-IT",
                "salesChannelCurrency": "EUR",
                "excludeCategories": [ 430 ]
        },
        {
                "salesChannelId": 13,
                "salesChannelIdentifier": "477097bb-8249-4fe5-85f1-ca44dbbf0e2f",
                "salesChannelName": "Platform-UK",
                "salesChannelCurrency": "GBP",
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

    sys.argv

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
        inp = input(f"Pres enter to create: {m['salesChannelName']}")
        logLineToBrowser(driver, f".")
        logLineToBrowser(driver, f"{m['salesChannelName']}", "large2")
        createVoucherForMarket(driver, m, f"Friends&Family{prefix}", 20, startDate, endDate)
        createVoucherForMarket(driver, m, f"MiintoEmployee{prefix}", 25, startDate, endDate)

    inp = input('All done. Press enter to exit!')
    driver.close()



if __name__ == "__main__":
    run()