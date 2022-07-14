# Installation

## Install requirements
    pip3 install -r requirements.txt

## Download webdriver for Chrome:
   
For m1/arm:

    wget https://chromedriver.storage.googleapis.com/$(curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_mac64_m1.zip

    unzip chromedriver_mac64_m1.zip

For x86:

    wget https://chromedriver.storage.googleapis.com/$(curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_mac64.zip
    unzip chromedriver_mac64.zip

## Copy chromedriver to path

    sudo cp chromedriver /usr/local/bin

## Run syntax
    python3 app.py <postfix> <date (dd-MM-yyyy)>

    # example: python3 app.py August235 01-09-2022