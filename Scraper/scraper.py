import os
import time
import datetime as dt
from PIL import Image, ImageOps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Set up chrome driver.
cwd = os.getcwd()
chrome_driver = cwd + "\\Scraper\\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")


class TpsScraper:
    def __init__(self) -> None:
        # URLs to pull data from.
        self.hedera_txns_url = "https://hederatxns.com/"
        self.coinmarketcap_url = "https://coinmarketcap.com/currencies/hedera/"
        self.hedera_revenue_url = "https://hedera.report/"
        self.tvl_url = "https://defillama.com/chain/Hedera"
        self.accounts_url = "https://app.dragonglass.me/hedera/home"

        # Class variables
        self.mainet_tps = None
        self.testnet_tps = None
        self.mainnet_txn = None
        self.testnet_txn = None
        self.market_cap = None
        self.price = None
        self.rank = None
        self.in_BTC = None
        self.network_revenue = None
        self.tvl = None
        self.accounts = None

    '''----------------------------------- Setters -----------------------------------'''

    def set_mainnet_transactions(self) -> None:
        try:
           # If the browser does not match the required url, it will be redirected to the correct url. 
            if self.browser.current_url != self.hedera_txns_url:
                self._redirect_browser(self.hedera_txns_url)
        except AttributeError:
          # If a browser object has not been created, it will be created and navigated to the desired url. 
            self.create_browser(self.hedera_txns_url)
        # Xpath to the element on the webpage.
        xpath = "/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/span[1]"
        # Read the data from the xpath. Remove the commas so we can turn it into an integer later. 
        self.mainnet_txn = int(self.read_data_wait(
            xpath=xpath).replace(",", ""))

    '''-----------------------------------'''

    def set_mainnet_tps(self) -> None:
        try:
            if self.browser.current_url != self.hedera_txns_url:
                self._redirect_browser(self.hedera_txns_url)
        except AttributeError:
            self.create_browser(self.hedera_txns_url)
        xpath = "/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/span[2]"
        self.mainet_tps = int(self.read_data_wait(
            xpath=xpath).split(" ")[0][1:])

    '''-----------------------------------'''

    def set_testnet_transactions(self) -> None:
        try:
            if self.browser.current_url != self.hedera_txns_url:
                self._redirect_browser(self.hedera_txns_url)
        except AttributeError:
            self.create_browser(self.hedera_txns_url)
        xpath = "/html/body/div[1]/div[2]/div/div[1]/div[2]/div[2]/span[1]"
        self.testnet_txn = int(self.read_data_wait(
            xpath=xpath).replace(",", ""))

    '''-----------------------------------'''

    def set_testnet_tps(self) -> None:
        try:
            if self.browser.current_url != self.hedera_txns_url:
                self._redirect_browser(self.hedera_txns_url)
        except AttributeError:
            self.create_browser(self.hedera_txns_url)
        xpath = "/html/body/div[1]/div[2]/div/div[1]/div[2]/div[2]/span[2]"
        self.testnet_tps = int(self.read_data_wait(
            xpath=xpath).split(" ")[0][1:])
    '''-----------------------------------'''

    def set_marketcap(self) -> None:
        try:
            if self.browser.current_url != self.coinmarketcap_url:
                self._redirect_browser(self.coinmarketcap_url)
        except AttributeError:
            self.create_browser(self.coinmarketcap_url)
        xpath = "/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div"
        self.market_cap = int(
            self.read_data_wait(xpath).replace(",", "")[1:])

    '''-----------------------------------'''

    def set_price(self) -> None:
        try:
            if self.browser.current_url != self.coinmarketcap_url:
                self._redirect_browser(self.coinmarketcap_url)
        except AttributeError:
            self.create_browser(self.coinmarketcap_url)
        xpath = "/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div/span"
        self.price = float(self.read_data_wait(xpath)[1:])

    '''-----------------------------------'''

    def set_rank(self) -> None:
        try:
            if self.browser.current_url != self.coinmarketcap_url:
                self._redirect_browser(self.coinmarketcap_url)
        except AttributeError:
            self.create_browser(self.coinmarketcap_url)
        xpath = "/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]"
        self.rank = int(self.read_data_wait(xpath).split(" ")[1][1:])

    '''-----------------------------------'''

    def set_in_BTC_terms(self) -> None:
        try:
            if self.browser.current_url != self.coinmarketcap_url:
                self._redirect_browser(self.coinmarketcap_url)
        except AttributeError:
            self.create_browser(self.coinmarketcap_url)
        xpath = "/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[2]/p[1]"
        self.in_BTC = self.read_data_wait(xpath).split(" ")[0]
        # Convert from scientific notation to long float.
        self.in_BTC = '{0:.9f}'.format(float(self.in_BTC))

    '''-----------------------------------'''

    def set_network_revenue(self) -> None:
        try:
            if self.browser.current_url != self.hedera_revenue_url:
                self._redirect_browser(self.hedera_revenue_url)
        except AttributeError:
            self.create_browser(self.hedera_revenue_url)
        xpath = "/html/body/flt-glass-pane"
        self.network_revenue = self.read_data_wait(xpath)

    def set_tvl(self) -> None:
        try:
            if self.browser.current_url != self.tvl_url:
                self._redirect_browser(self.tvl_url)
        except AttributeError:
            self.create_browser(self.tvl_url)
        xpath = "/html/body/div[1]/div/main/div[2]/div[1]/div[1]/p"
        self.tvl = self.read_data_wait(xpath)
        self.tvl = self._format_number(self.tvl)

    '''-----------------------------------'''

    def set_accounts(self) -> None:
        try:
            if self.browser.current_url != self.accounts_url:
                self._redirect_browser(self.accounts_url)
        except AttributeError:
            self.create_browser(self.accounts_url)
        xpath = "/html/body/div[1]/div/div[2]/div/div/div/div/div[4]/div/div[1]/div/div[2]/div/div[4]/span"
        time.sleep(5)
        self.accounts = self.read_data_wait(xpath, wait_time=10)
        self.accounts = int(self.accounts.replace(",", ""))

    '''----------------------------------- Getters -----------------------------------'''

    def get_mainnet_transactions(self) -> int:
      # If class variable has not been assigned, call the "set" fucntion relative to the class variable. 
        if self.mainnet_txn == None:
            self.set_mainnet_transactions()
      # Return the data. 
        return self.mainnet_txn

    '''-----------------------------------'''

    def get_mainnet_tps(self) -> int:
        if self.mainet_tps == None:
            self.set_mainnet_tps()
        return self.mainet_tps

    '''-----------------------------------'''

    def get_testnet_transactions(self) -> int:
        if self.testnet_txn == None:
            self.set_testnet_transactions()
        return self.testnet_txn

    '''-----------------------------------'''

    def get_testnet_tps(self) -> int:
        if self.testnet_tps == None:
            self.set_testnet_tps()
        return self.testnet_tps

    '''-----------------------------------'''

    def get_marketcap(self) -> str:
        if self.market_cap == None:
            self.set_marketcap()
        return self.market_cap

    '''-----------------------------------'''

    def get_price(self) -> str:
        if self.price == None:
            self.set_price()
        return self.price

    '''-----------------------------------'''

    def get_rank(self) -> str:
        if self.rank == None:
            self.set_rank()
        return self.rank

    '''-----------------------------------'''

    def get_in_BTC(self) -> float:
        if self.in_BTC == None:
            self.set_in_BTC_terms()
        return self.in_BTC

    '''-----------------------------------'''

    def get_network_revenue(self) -> int:
        if self.network_revenue == None:
            self.set_network_revenue()
        return self.network_revenue

    '''-----------------------------------'''

    def get_tvl(self) -> int:
        if self.tvl == None:
            self.set_tvl()
        return self.tvl

    '''-----------------------------------'''

    def get_accounts(self) -> int:
        if self.accounts == None:
            self.set_accounts()
        return self.accounts

    '''----------------------------------- Utilities -----------------------------------'''

    def read_data_wait(self, xpath: str, wait_time: int = 5):
      # Wait for element to appear on the page for a designated duration. If the element appears within the duration the text will be returned. 
        element = WebDriverWait(self.browser, wait_time).until(
            EC.presence_of_element_located((By.XPATH, xpath))).text

        return element
    '''-----------------------------------'''

    def read_data(self, xpath: str):
        # Find the element by xpath and extract the text. 
        data = self.browser.find_element("xpath", xpath).text
        return data

    '''-----------------------------------'''

    def create_browser(self, url=None):
      # Create chrome driver object with the respective options. 
        self.browser = webdriver.Chrome(
            executable_path=chrome_driver, chrome_options=chrome_options)
        # Defautl browser route
        if url == None:
            self.browser.get(url=self.hedera_txns_url)
        # External browser route
        else:
            self.browser.get(url=url)

    '''-----------------------------------'''

    def close_browser(self):
        self.browser.close()

    '''-----------------------------------'''

    def create_screenshot(self) -> None:
      # Create a filename for the screenshot.
        file_name = self.create_image_filename()
        
        self.browser.get_screenshot_as_file(file_name)
        self.resize_image(file_name=file_name)

        # This is to resize the image to custom dimensions.

    '''-----------------------------------'''

    def create_image_filename(self) -> str:
      # Creates a filename with the current working directory.
        return cwd + "\\Scraper\\Screenshots\\" + "TPS_" + \
            str(dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")) + ".png"

    '''-----------------------------------'''

    def resize_image(self, file_name: str):
        # Base image should be 1877 x 1872

        # Create an object for the image file.
        img = Image.open(file_name)
        # Get the dimensions of the image.
        width, height = img.size

        # Adjust how high the crop window is. The higher the number, the higher the window is, vertically.
        height_adjust = 20

        # Size of the window
        vertical_window_size = 10

        left = 300
        top = height / height_adjust
        right = 1572
        bottom = vertical_window_size * height / height_adjust

        img1 = img.crop((left, top, right, bottom))

        img1.save(file_name)

    '''-----------------------------------'''

    def _redirect_browser(self, url: str) -> None:
        self.browser.get(url)

    '''-----------------------------------'''

    def _format_number(self, num: str) -> int:
        num, extension = float(num[1:-1]), num[-1]

        if extension == "m" or extension == "M":
            multiplier = 1000000
        elif extension == "b" or extension == "B":
            multiplier = 1000000000
        elif extension == "t" or extension == "T":
            multiplier = 1000000000000
        num *= multiplier
        return int(num)

