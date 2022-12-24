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
    root.destroy()


def selenium_driver():
    # options setting and return chrome driver url
    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # If the Chrome version is low, an error occurs
    driver_url = webdriver.Chrome('chromedriver.exe', options=options)
    return driver_url


def run():
    # execute tor browser, if running tor browser, kill process
    for proc in psutil.process_iter():
        if proc.name() == 'Tor Browser':
            proc.kill()

    path = os.getcwd() + "\\Tor Browser\\Browser\\firefox.exe"

    os.system('"{0}"'.format(path))
    time.sleep(10)

    # change url to string
    url = str(url_entry.get())
    # execute chrome driver
    driver = selenium_driver()
    driver.get(url)
    time.sleep(600)
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

exit_button = Button(root, text="종료", command=threading_exit)
exit_button.pack()

root.mainloop()
