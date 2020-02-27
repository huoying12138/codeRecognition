# -*- coding: utf8
# @Time: 2020/2/25 14:17
# @Author: Blue_Sky
# @File: codetest.py
# @descriptions: none
from io import BytesIO

from PIL import Image
from selenium.webdriver import ActionChains

from codeRecognition.chaojiying import Chaojiying_Client
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import quote
from pyquery import PyQuery as pq
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import os
import time
import requests
import pymongo

Email = ''
Password = ''
Url = 'https://www.163yun.com/trial/picture-click'
Chao_username = 'huoying12138'
Chao_password = '369369369aaa'
Chao_softid = '903630'
Chao_codetype = 9103


class CrackTouClick:
    def __init__(self):
        self.url = Url
        self.browser = webdriver.Chrome()
        self.browser.get(self.url)
        self.wait = WebDriverWait(self.browser, 10)
        self.email = Email
        self.password = Password
        self.chaojiying = Chaojiying_Client(Chao_username, Chao_password, Chao_softid)

    def open(self):
        pass

    def get_button(self):
        button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_tips')))
        return button

    def get_image(self):
        image = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img[class="yidun_bg-img"]')))
        return image

    def get_elem(self):
        elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="yidun_panel"]')))
        return elem

    def get_chao_position(self):
        image = self.get_image()
        url = image.get_attribute('src')
        with open('a.jpg', 'wb+') as f:
            f.write(requests.get(url).content)
        if os.path.exists('a.jpg'):
            im = open('a.jpg', 'rb').read()
            return self.chaojiying.PostPic(im, Chao_codetype)
        else:
            print('图片发送超级鹰失败')

    def get_chao_position_2(self):
        image = self.get_screen_click()
        i = image.resize((320, 215))
        if os.path.exists('b.png'):
            os.remove('b.png')
            print('remove b.png')
        i.save('b.png')
        im = open('b.png', 'rb').read()
        res = self.chaojiying.PostPic(im, Chao_codetype)
        print(res)
        return res


    def get_position(self):
        image = self.get_button()
        time.sleep(1)
        location = image.location
        size = image.size
        print("location：", location)
        print("size：", size)
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        top = top - 160
        return top, bottom, left, right

    def get_screenshot(self):
        time.sleep(9)
        ActionChains(self.browser).move_to_element(self.get_button()).perform()
        time.sleep(9)
        if os.path.exists('all.png'):
            os.remove('all.png')
            print('remove all.png')
        self.browser.get_screenshot_as_file('all.png')
        screenshot = Image.open('all.png')
        return screenshot

    def get_screen_click(self):
        # top, bottom, left, right = self.get_position()
        left, top, right, bottom = 420, 540, 823, 811
        print("验证码截图位置：", left, top, right, bottom)
        screenshot = self.get_screenshot()
        return screenshot.crop((left, top, right, bottom))

    def get_points(self):
        position = self.get_chao_position_2()
        groups = position.get('pic_str').split('|')
        if position.get('err_no') == 0:
            locations = [[int(number) for number in group.split(',')] for group in groups]
            return locations
        else:
            print(position)

    def click_image(self):
        locations = self.get_points()
        print(locations)
        ActionChains(self.browser).move_to_element(self.get_button()).perform()
        for location in locations:
            print(location)
            ActionChains(self.browser).move_to_element_with_offset(self.get_elem(), location[0], location[1]).click().perform()
            time.sleep(0.15)

    def is_success(self):
        elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="yidun_tips"] >span.yidun_tips__text')))
        print(elem.text)
        if elem.text == '验证成功':
            return True
        else:
            return False


if __name__ == '__main__':
    c = CrackTouClick()
    while not c.is_success():
        c.get_button()
        c.click_image()