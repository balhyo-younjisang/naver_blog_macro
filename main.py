from tkinter import *
import time
import threading
import schedule
# using selenium for chrome driver control
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import psutil

# Tk setup
root = Tk()
root.title("Naver Macro")
root.geometry("900x300")
root.resizable(False, False)


def threading_exit():
    th = threading.Thread(target=quit_program)
    th.daemon = True
    th.start()


def threading_init():
    th = threading.Thread(target=init)
    th.daemon = True
    th.start()


def quit_program():
    for proc in psutil.process_iter():
        if proc.name() == 'Google Chrome':
            proc.kill()

    for proc in psutil.process_iter():
        if proc.name() == 'Tor Browser' or proc.name() == 'firefox.exe':
            proc.kill()
    root.destroy()


def selenium_driver():
    # options setting and return chrome driver url
    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # If the Chrome version is low, an error occurs
    # driver_url = webdriver.Chrome('chromedriver.exe', options=options)
    driver_url = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver_url


def run():
    path = os.getcwd() + "\\Tor Browser\\Browser\\firefox.exe"

    os.system('"{0}"'.format(path))
    time.sleep(10)

    # change url to string
    url = str(url_entry.get())
    # execute chrome driver
    driver = selenium_driver()
    driver.delete_all_cookies()
    driver.get(url)
    time.sleep(600)
    driver.quit()

    for proc in psutil.process_iter():
        if proc.name() == 'Tor Browser' or proc.name() == 'firefox.exe':
            proc.kill()


def init():
    # every 10 minute, execute run function
    schedule.every(11).minutes.do(run)
    run()

    while True:
        schedule.run_pending()
        time.sleep(1)


url_entry = Entry(root, width=20)
url_entry.insert(0, "URl 입력")
url_entry.pack()

url_input_button = Button(root, text="이 링크로 실행", command=threading_init, width=20, height=2, font=('맑은 고딕', 10, 'bold'), bg='#2F5597', fg='white', )
url_input_button.pack()

exit_button = Button(root, text="종료", command=threading_exit, width=20, height=2, font=('맑은 고딕', 10, 'bold'), bg='#2F5597', fg='white')
exit_button.pack()

root.mainloop()
