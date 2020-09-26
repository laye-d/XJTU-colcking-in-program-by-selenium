# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 10:38:50 2020

@author: a3620
"""

#浏览器控制
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
#鼠标键盘控制
import pyautogui
#时间
import time
#运行超时跳过
#import eventlet  

#*************INFO****************
#主页面
url = "http://equip.xjtu.edu.cn/home/"
#设备预约页面
url_2 = "http://equip.xjtu.edu.cn/lims/!equipments/equipment/index.994.reserv"
#url_2 = "http://equip.xjtu.edu.cn/lims/!equipments/equipment/index.972.reserv"
#用户信息
username = "username"
pwd = "password"
#待预约时间点的屏幕像素位置
position_x = 1350
position_y = 328
#位置测试
#pyautogui.moveTo(position_x,position_y)
#********************************

#登录并进入预约页面
browser = webdriver.Chrome()
browser.get(url)
browser.implicitly_wait(20)
elem=browser.find_element_by_id("top_4")
elem.click()
browser.implicitly_wait(20)
elem=browser.find_element_by_name("username")
elem.send_keys(username)
elem=browser.find_element_by_name("pwd")
elem.send_keys(pwd)
elem=browser.find_element_by_id("account_login")
elem.click()
time.sleep(10)
browser.get(url_2)

class alert_is_present(object):
    """ Expect an alert to be present."""
    """判断当前页面的alert弹窗"""
    def __init__(self):
        pass

    def __call__(self, driver):
        try:
            alert = driver.switch_to.alert
            alert.text
            return alert
        except NoAlertPresentException:
            return False

#暂停运行。手动调整页面，至待预约时间点到该屏幕位置。
time.sleep(20)
time.sleep(5)
refresh_success = False;
#运行超时跳过
#eventlet.monkey_patch() 

#循环刷新，成功后自动填写验证码以外的预约信息。手动填写验证码并提交。
while True:

		#双击并等待响应
        pyautogui.doubleClick(position_x,position_y)
        time.sleep(2.5)

#        #运行超时跳过
#        with eventlet.Timeout(1,False):
#            try: 
#                result = browser.find_element_by_name("save")
#            except:

        #先判断是否有弹窗（因为无alert时，alert_is_present()函数耗时较长）
        result_alert = EC.alert_is_present()(browser)
        #try预约框元素，若有，则并填写预约信息
        if not result_alert:
                     try: 
                         elem = browser.find_element_by_name("description")
                         elem.send_keys("1")
                         #动态id的Xpath定位
#                         elem = browser.find_element_by_xpath("//input[@value='无' and @name='extra_fields[2]']")
#                         elem.click()
                         elem = browser.find_element_by_name("extra_fields[1][委托操作]")
                         elem.click()
                         elem = browser.find_element_by_name("extra_fields[2][块体]")
                         elem.click()
                         elem = browser.find_element_by_name("extra_fields[5][否]")
                         elem.click()
                         elem = browser.find_element_by_name("extra_fields[6][其他]")
                         elem.click()
                         elem = browser.find_element_by_name("extra_fields[25][形貌观察]")
                         elem.click()
                         elem = browser.find_element_by_name("extra_fields[3]")
                         elem.send_keys("1")
                         elem = browser.find_element_by_name("extra_fields[4]")
                         elem.send_keys("1")
                         elem = browser.find_element_by_name("extra_fields[23]")
                         elem.send_keys("1")
                         elem = browser.find_element_by_name("extra_fields[24]")
                         elem.send_keys("1")
                         elem = browser.find_element_by_name("captcha")
                         elem.send_keys("1")
                         refresh_success = True
                         print("refresh success")
                         break
                     except:
                         print("No target element found, retry...")
        #关闭alert弹窗
        while True:
                result_alert = EC.alert_is_present()(browser)
                if result_alert:
                    print (result_alert.text)
                    result_alert.accept()
                    break
                else: pyautogui.doubleClick(position_x,position_y)

#刷新任务完成        
print (refresh_success)                

