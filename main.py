from tracemalloc import start
import numpy as np
import pandas as pd
import bs4
from bs4 import BeautifulSoup
import requests
import csv
import datetime
import time

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class AmazonOrderScraper:

    def __init__(self):
        self.date = np.array([])
        self.cost = []
        self.order_id = np.array([])

    def URL(self, year, start_index):
        return "https://www.amazon.com/gp/your-account/order-history/" + \
            "ref=ppx_yo_dt_b_pagination_1_2?ie=UTF8&orderFilter=year-" + \
                str(year) + \
                    "&search=&startIndex=" + str(start_index)

    def scrape_order_data(self, start_year, end_year):
        years = list(range(start_year, end_year + 1))
        driver = self.start_driver_and_manually_login_to_amazon()

        for year in years:
            offset = 0
            while True:
                try:
                    driver.get(
                        self.URL(year, offset)
                    )
            
                    offset += 10
                    if self.scrape_first_page_before_progressing(driver) == []:
                        break

                except:
                    continue

    def start_driver_and_manually_login_to_amazon(self):
        driver = webdriver.Chrome()
        amazon_sign_in_url = "https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_custrec_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&"

        driver.get(amazon_sign_in_url)
        time.sleep(15) # allows time for manual sign in - increase if you need more time
        
        
        return driver

    def scrape_first_page_before_progressing(self, driver):
        # time.sleep(2)
        page_source = driver.page_source
        page_content = BeautifulSoup(page_source, "html.parser")

        order_info = page_content.findAll("span", {"class": "a-color-secondary value"})

        orders = []

        for order in order_info:
            orders.append(order.text.strip())
        
        index = 0
        for i in orders:
            if index == 0:
                self.date = np.append(self.date, i)
                index += 1
            elif index == 1:
                i = i.replace("$", "")
                i = float(i)
                self.cost.append(i)
                index += 1
            elif index == 2:
                self.order_id = np.append(self.order_id, i)
                index = 0
        print(orders)
        return orders

if __name__ == "__main__":

    x = AmazonOrderScraper()
    x.scrape_order_data(2013, 2021)
    print(sum(x.cost))