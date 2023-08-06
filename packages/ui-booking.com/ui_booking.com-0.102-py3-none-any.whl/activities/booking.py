import slash
from selenium import webdriver
import booking.constants as const
import time
from selenium.webdriver.common.by import By

class Booking(webdriver.Chrome):
    def __init__(self):
        super(Booking, self).__init__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)
        time.sleep(999999999999999999999)


    def handle_popup(self):
        self.find_element(by=By.CSS_SELECTOR, value="span[class='b6dc9a9e69 e25355d3ee']").click()


