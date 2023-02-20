### Automate PVLive data download

This folder consists of web-scraping functions using [Selenium Python](https://selenium-python.readthedocs.io/) and [Webdriver-manager](https://pypi.org/project/webdriver-manager/) and `datapipes` to automate the data download and other configurations.

### Usage

Install the necessary packages
```bash
pip install selenium
pip install webdriver-manager
```

Create a folder in the root to store the google-chrome files
```bash
cd
mkdir usr/bin/google-chrome
```

If the user is working on Windows, download only the chrome driver into the above `google-chrome` directory. `Chrome Driver` can be downloaded [here](https://chromedriver.chromium.org/downloads). If the user is on the Ubuntu Linux distribution, follow the below steps.

Move to the google-chrome directory that has been created in the previous steps.

Download and install the chrome browser
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

Download and unzip the chrome driver.
```bash
wget https://chromedriver.storage.googleapis.com/111.0.5563.19/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
```

