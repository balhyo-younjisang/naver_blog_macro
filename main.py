from tkinter import *
import time
import threading
import schedule
# using selenium for chrome driver control
from selenium import webdriver
import os
import psutil

# Tk setup
root = Tk()
root.title("Naver Macro")
root.geometry("900x300")
root.resizable(False, False)


def threading_init():
    th = threading.Thread(target=init)
    th.daemon = True
    th.start()


def selenium_driver():
    # options setting and return chrome driver url
    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
    #options.add_argument("headless")
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # If the Chrome version is low, an error occurs
    driver_url = webdriver.Chrome('chromedriver.exe', options=options)
    return driver_url


def run():
    # execute tor browser, if running tor browser, kill process
    for proc in psutil.process_iter():
        if proc.name() == 'firefox.exe':
            proc.kill()

    # path = os.path.dirname(__file__) + "\\Tor Browser\\Browser\\firefox.exe"
    path = os.getcwd() + "\\Tor Browser\\Browser\\firefox.exe"

    os.system('"{0}"'.format(path))
    time.sleep(10)

    # change url to string
    url = str(url_entry.get())
    # execute chrome driver
    driver = selenium_driver()
    driver.get(url)
    time.sleep(3600)
    driver.quit()


def init():
    # every 10 minute, execute run function
    run()
    schedule.every(10).minutes.do(run)

    while True:
        schedule.run_pending()
        time.sleep(1)


url_entry = Entry(root)
url_entry.pack()

url_input_button = Button(root, text="이 링크로 실행", command=threading_init)
url_input_button.pack()

root.mainloop()
