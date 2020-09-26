# -*- coding: utf-8 -*-
"""
@author: a3620
"""

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import sys
import datetime
import getpass

#*************INFO****************
url = "http://jkrb.xjtu.edu.cn/EIP/user/index.htm"

print(">> Enter the username:")
username = input()
print(">> Enter the password of username '"+username+"':")
pwd = getpass.getpass()
print('>> Enter the last clocking-in: (e.g. 20200831)')
lastDay = float(input())
print('>> Enter the time delay for clocking-in: (in minutes)')
delay = float(input())
#******************************

#get path whether running from Python or an exe file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def run ():
    print(">> Running.")
    browser = webdriver.Chrome(resource_path('./SeleniumDriver/chromedriver.exe'))

    while True:
        try:
            browser.get(url)
            browser.implicitly_wait(20)
            try:
                elem=browser.find_element_by_name("username")
                elem.send_keys(username)
                elem=browser.find_element_by_name("pwd")
                elem.send_keys(pwd)
                elem=browser.find_element_by_id("account_login")
                elem.click()
                browser.implicitly_wait(20)
                time.sleep(1)
            except:
                print("Already logged in.")
            
            
             #打开研究生每日健康状况填报
            browser.switch_to.default_content()#跳回最外层的页面
            iframe = browser.find_element_by_xpath("//*[@id='mini-17$body$2']/iframe")
            browser.switch_to.frame(iframe)
            iframe = browser.find_element_by_xpath("//*[@id='ab0ab54c0e7048a7b583d5c1c8da7c06']/div/div[2]/div[2]/iframe")
            browser.switch_to.frame(iframe)
            elem = browser.find_element_by_xpath("//div[@title='研究生每日健康状况填报']")
            elem.click()
            browser.implicitly_wait(20)
            time.sleep(1)
            
            
            #打开每日健康填报
            browser.switch_to.default_content()#跳回最外层的页面
#            iframe = browser.find_element_by_xpath("//*[@id='mini-17$body$2']/iframe")
            iframe = browser.find_element_by_xpath("//*[@id='mini-17$body$3']/iframe")
            browser.switch_to.frame(iframe)
#            iframe = browser.find_element_by_xpath("//*[@id='ab0ab54c0e7048a7b583d5c1c8da7c06']/div/div[2]/div[2]/iframe")
#            browser.switch_to.frame(iframe)
#            elem = browser.find_element_by_xpath("//div[@title='研究生每日健康状况填报']")
            elem = browser.find_element_by_xpath("//span[@title='每日健康填报']")
            elem.click()
            browser.implicitly_wait(20)
            time.sleep(1)
            
            
            #填写内容
            browser.switch_to.default_content()
            iframe = browser.find_element_by_xpath("//*[@id='mini-17$body$4']/iframe")
            browser.switch_to.frame(iframe)
            iframe = browser.find_element_by_xpath("//*[@id='mini-14$body$2']/iframe")
            browser.switch_to.frame(iframe)
            elem = browser.find_element_by_xpath("//input[@value='绿色']")
            elem.click()
#            elem = browser.find_element_by_xpath("//input[@id='mini-72$ck$0']")
            elem = browser.find_element_by_xpath("//input[@value='我已阅知']")
            elem.click()
            elem = browser.find_element_by_xpath("//input[@value='是']")
            elem.click()            
            elem = browser.find_element_by_xpath("//input[@name='BRTW']")
            elem.send_keys("36.5")
            
            
            #提交
            browser.switch_to.parent_frame()#切到父frame
            elem = browser.find_element_by_xpath("//a[@id='sendBtn' and @onclick='onSend()']")
            elem.click()
            browser.implicitly_wait(20)
            time.sleep(1)
            elem = browser.find_element_by_xpath("//span[@class='mini-button-text ']")
            elem.click()
            print(">> Done.")
            state_succeed = True
            break
        except:
            time_now = datetime.datetime.now()
            if (time_now.hour+time_now.minute/100 < 17.00):
                print(">> An error occurred. Retry...")
            else:
                print(">> Later than 5 pm. Quit browser...")
                print(">> Failed. ")
                state_succeed = False
                break
    #关闭
    browser.quit()
    return state_succeed
    



#while True:
#    time_now = datetime.datetime.now()
##    time_now = time.strftime("%a %b %d %Y %H:%M:%S", time.localtime()) 
#    currentDay = time_now.year*10000+time_now.month*100+time_now.day
#    if time_now.hour+time_now.minute/100 > 12:
#        currentDay = currentDay + 0.5
#    if currentDay > lastDay:
#        if ((6.00+delay/100)< time_now.hour+time_now.minute/100 \
#                and time_now.hour+time_now.minute/100 < 11.00) \
#            or ((12.00+delay/100)< time_now.hour+time_now.minute/100 \
#                and time_now.hour+time_now.minute/100 < 17.00):
#            run()
#            lastDay = currentDay
#            print(">> Last clocking-in: "+str(currentDay))
#    print(">> Time: " + str(time_now),end = "")
#    print("\b" * len(">> Time: " + str(time_now)),end = "",flush=True)
#    time.sleep(1)
#    
lastCDay = lastDay
while True:
    time_now = datetime.datetime.now()
    currentDay = time_now.year*10000+time_now.month*100+time_now.day
    if currentDay > lastDay:
        if ((6.00+delay/100)< time_now.hour+time_now.minute/100 \
                and time_now.hour+time_now.minute/100 < 17.00):
            state_succeed = run()
            if state_succeed:
                lastCDay = currentDay
                print(">> Last clocking-in: "+str(lastCDay))
            else:
                print(">> Last clocking-in: "+str(lastCDay))
            lastDay = currentDay
    print(">> Time: " + str(time_now),end = "")
    print("\b" * len(">> Time: " + str(time_now)),end = "",flush=True)
    time.sleep(1)
