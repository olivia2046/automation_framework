# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/18 18:37
# @Author : Olivia
# Desc:
# **************************************
# This sample code supports Appium Python client >=2.3.0
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

options = AppiumOptions()
options.load_capabilities({
	"platformName": "Android",
	"appium:platformVersion": "13",
	"appium:deviceName": "5e5984e21223",
	"appium:appPackage": "com.bizlog.triplog",
	"appium:appActivity": "com.esocialllc.triplog.module.setup2.SetupActivity2",
	"appium:newCommandTimeout": 6000,
	"appium:noReset": False, #必须设置为false才能启动
	"appium:autoGrantPermissions": True,
	"appium:automationName": "UiAutomator2",
	#"appium:waitActivity": "com.esocialllc.triplog.module.setup2.LoginActivity2",

})

driver = webdriver.Remote("http://localhost:4723", options=options)


driver.quit()