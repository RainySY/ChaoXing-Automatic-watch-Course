# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/3/22 13:05
# @Author: 冬酒暖阳
# @File  : signIn.py


def QR_code_sign_in(browser):
    print("!!!!!!!!!!!!!!!!!!!!")
    browser.switch_to.frame('iframe')
    QR_code_element = browser.find_element_by_xpath(
        '/html/body/div/div/div/img')  # 获取登录二维码所在标签
    print(QR_code_element)
    print("!!!!!!!!!!!!!!!!!!!!")
    QR_code_src = QR_code_element.get_attribute("src")
    print(QR_code_src)
    from requests import get
    QR_code = get(QR_code_src).content

    with open('qr_code.png', 'wb') as qr:
        qr.write(QR_code)
    from PIL import Image
    QR_img = Image.open('qr_code.png')
    QR_img.show()
    from selenium.webdriver.support import ui
    wait = ui.WebDriverWait(browser, 310)
    wait.until(lambda wait_driver: browser.find_element_by_xpath(
        '//*[@id="leftmodule"]/div[2]/div/p'))
    try:
        user_name = browser.find_element_by_xpath(
            '//*[@id="leftmodule"]/div[2]/div/p').text
    except:
        user_name = ""
    #     refrush_CQ_code = browser.find_element_by_xpath('/html/body/div/div[1]/div/div/a')
    #     refrush_CQ_code.click()
    #     QR_code_sign_in(browser.switch_to_default_content())
    if user_name:
        return True
    else:
        return False


def input_usename_and_password(browser):
    inp = input("请输入账号:")
    inp_2 = input("请输入密码:")
    # # inp_3=input("请输入验证码:")
    # inp_3 = input("请输入验证码:")
    browser.find_element_by_xpath(
        '/html/body/div/div[2]/div/div[1]/div[1]/ul/li[2]').click()

    username = browser.find_element_by_id("uin_tips")
    password = browser.find_element_by_id("pwd_tips")
    # verycode = browser.find_element_by_id("numcode")
    username.send_keys(inp)
    password.send_keys(inp_2)
    # verycode.send_keys(inp_3)
    sbm = browser.find_element_by_id("login")
    # sleep(1)
    sbm.click()


# def main_signIn(browser):
#     sign_in_type = int(input("请输入登录方式：（1、扫码，2、账号密码登录）："))
#     if sign_in_type == 1:
#         QR_code_sign_in(browser)


def wait_sign_in(browser):
    from selenium.webdriver.support import ui
    # wait = ui.WebDriverWait(browser, 305)
    try:
        wait = ui.WebDriverWait(browser, 305)
        wait.until(lambda wait_driver: browser.find_element_by_xpath(
            '//*[@id="leftmodule"]/div[2]/div/p'))
        # wait.until(browser.find_element_by_xpath(
        #     '//*[@id="leftmodule"]/div[2]/div/p'))
        # user_name = browser.find_element_by_xpath(
        #     '//*[@id="leftmodule"]/div[2]/div/p').text
    except:
        # user_name = ""
        return False
    #     refrush_CQ_code = browser.find_element_by_xpath('/html/body/div/div[1]/div/div/a')
    #     refrush_CQ_code.click()
    #     QR_code_sign_in(browser.switch_to_default_content())
    else:
        return True


def check_sign_in(browser):
    while not wait_sign_in(browser):
        # print("二维码已失效！准备刷新！")
        browser.switch_to.frame('iframe')
        browser.find_element_by_xpath(
            '/html/body/div/div[1]/div/div/a').click()
        browser.switch_to_default_content()
    user_name = browser.find_element_by_xpath(
        '//*[@id="leftmodule"]/div[2]/div/p').text
    return user_name


if __name__ == "__main__":
    from selenium import webdriver  # 导入库
    from time import sleep
    browser = webdriver.Chrome(
        executable_path="./chromedriver.exe")  # 双引号内添加浏览器驱动的地址
    # browser = webdriver.Edge(executable_path="./msedgedriver.exe")
    url = "http://i.chaoxing.com/"  # 这里改成自己学校的学习通登录地址
    browser.get(url)
    # sleep(10)
    # main_signIn(browser)

    # browser.quit()
