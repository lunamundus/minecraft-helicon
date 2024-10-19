from mcpi.minecraft import Minecraft
from pyowm import OWM

import modi
import pydirectinput
import pyautogui
import datetime
import time

# OpenWeatherMap으로부터 날씨 정보 받아오기
def weather_check(api_key):
    API_key = api_key
    owm = OWM(API_key)
    mgr = owm.weather_manager()
    obs = mgr.weather_at_place('Seoul')
    w = obs.weather
    WEATHER = w.status
    weather = WEATHER.lower()
    
    if weather == 'rain':
        weather = 'rain'
    else:
        weather = 'clear'
    
    return weather


# 현재 시간 불러오기
def current_time():
    now_time = datetime.datetime.now().hour
    mc_time = (now_time - 6)*1000
    change_time = 'time set ' + str(mc_time)
    
    return change_time


# 자이로센서 모듈을 이용한 게임 컨트롤
def game_control(gyro):
    if gyro.roll > 10:
        pydirectinput.keyDown('s')
        if gyro.pitch > 10:
            pydirectinput.keyDown('a')
        elif gyro.pitch < -10:
            pydirectinput.keyDown('d')
        else:
            pydirectinput.keyUp('a')
            pydirectinput.keyUp('d')
    elif gyro.roll < -10:
        pydirectinput.keyDown('w')
        if gyro.pitch > 10:
            pydirectinput.keyDown('a')
        elif gyro.pitch < -10:
            pydirectinput.keyDown('d')
        else:
            pydirectinput.keyUp('a')
            pydirectinput.keyUp('d')
    else:
        pydirectinput.keyUp('s')
        pydirectinput.keyUp('w')
        pydirectinput.keyUp('a')
        pydirectinput.keyUp('d')
    
    if gyro.pitch > 10:
        pydirectinput.keyDown('a')
    elif gyro.pitch < -10:
        pydirectinput.keyDown('d')
    else:
        pydirectinput.keyUp('a')
        pydirectinput.keyUp('d')
        
    if btn.pressed:
        pydirectinput.keyDown('ctrl')
    else:
        pydirectinput.keyUp('ctrl')


mc = Minecraft.create()

bundle = modi.MODI()

gyro = bundle.gyros[0]
btn = bundle.buttons[0]

start = True

# 게임 조작
while True:
    game_control(gyro)
    
    # 처음 게임을 시작했을 때, 현재 시간 및 날씨 세팅
    if start:
        pydirectinput.press('/')
        pyautogui.typewrite('gamerule doDaylightCycle false')
        pydirectinput.press('enter')
        pydirectinput.press('/')
        pyautogui.typewrite(f'time set {current_time()}')
        pydirectinput.press('enter')
        pydirectinput.press('/')
        pyautogui.typewrite(f'weather {weather_check(api_key="")}') # API 키는 발급받아 사용
        pydirectinput.press('enter')
        start = False