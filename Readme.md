# Installation

## Clone solution

Clone repository locally

    git clone https://github.com/silashansen/v_automation.git

Step into the solution directory

    cd v_automation/

## Install requirements

**Make sure your pip is updated*:exclamation:

    pip3 install -r requirements.txt

## Download webdriver for Chrome:
Select your architecture below
   
### For m1:

    wget https://chromedriver.storage.googleapis.com/$(curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_mac64_m1.zip

    unzip chromedriver_mac64_m1.zip

### For x86:

    wget https://chromedriver.storage.googleapis.com/$(curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_mac64.zip

    unzip chromedriver_mac64.zip

## Copy chromedriver to path

    sudo cp chromedriver /usr/local/bin

## Run syntax
    python3 app.py <postfix> <date (dd-MM-yyyy)>

    # example: python3 app.py August235 01-09-2022
