# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:22:35 2019

@author: a3620
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
#from pyquery import PyQuery as pq
#import re
import time

#*************信息****************
url = "http://119.23.30.128/login/"
username = "username"
pwd = "password"
#********************************

#浏览器登录
browser = webdriver.Chrome()
browser.get(url)
browser.implicitly_wait(20)#隐性等待
elem=browser.find_element_by_name("username")
elem.send_keys(username)
elem=browser.find_element_by_name("password")
elem.send_keys(pwd)
elem=browser.find_element_by_xpath("/html/body/div/form/input[3]")
elem.click()

#打开我的预约
browser.switch_to.window(browser.window_handles[-1])#切换窗口句柄到新网页
elem=browser.find_element_by_xpath("/html/body/div[2]/div[1]/div/ul[2]/li[1]/a")
elem.click()

#始终运行自动登记
while True:
    try:
        # 每隔0.5分钟刷新检查有无待登记项目
        all_checkin_element = []
        while len(all_checkin_element) == 0:
            while True:
                try:
                    browser.refresh()
                    break
                except:
                    print("刷新出现异常，重试...")
            # 通过CSS定位
            all_checkin_element = browser.find_elements_by_css_selector(
                "[style = 'color: white;background-color: #1b54b4;padding-left: 20%;padding-right: 20%']")
            time.sleep(20)
            # length = len(all_checkin_element)
        # 登记项目
        while len(all_checkin_element) > 0:
            all_checkin_element[0].click()
            # 显性等待，直至出现元素
            locator = (By.XPATH, "/html/body/div[4]/div[3]/div/button[1]")
            WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(locator))
            time.sleep(2)  # 等待
            browser.find_element_by_xpath("/html/body/div[4]/div[3]/div/button[1]").click()
            time.sleep(20)  # 等待
            browser.switch_to.alert.accept()  # 弹出警告窗口确定
            time.sleep(2)  # 等待
            all_checkin_element = browser.find_elements_by_css_selector(
                "[style = 'color: white;background-color: #1b54b4;padding-left: 20%;padding-right: 20%']")
    except:
        print("程序异常，重试...")



#返回待登记项目总数
#return(length)
#browser.close()

# 打印所有的handle
#all_handles = browser.window_handles
#print(all_handles)
# 切换到新的handle上
#browser.switch_to.window(all_handles[1])    
    
    
