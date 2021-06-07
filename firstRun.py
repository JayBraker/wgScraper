#!/home/jaybraker/venvs/wggesucht/venv/bin/python3
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import telegramNotify
import argparse
import time

class webInterface:
    def __init__(self, username: str, password: str, notify = None):
        """
        :param username: Username or E-mail for Log-in in Instagram
        :param password: Password for Log-in in Instagram
        :param url: Login Url
        """
        self.username = username
        self.password = password
        self.url: str = "https://www.wg-gesucht.de"
        self.notify = notify
        chromeOptions = Options()
        chromeOptions.headless = True
        self.driver = webdriver.Chrome('/home/jaybraker/venvs/selenium/chromedriver', options=chromeOptions)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    def login(self):
        self.driver.get(self.url)

        try:
            submit = self.driver.find_element_by_link_text("Accept all")
            submit.click()
        except:
            print("Kein DSGVO Banner")

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'col-sm-8')))
        submit = self.driver.find_element_by_class_name("col-sm-8")
        submit = submit.find_elements_by_css_selector("a")[1]
        submit.click()

        time.sleep(5)
        self.driver.find_element_by_name('login_email_username').send_keys(self.username)
        time.sleep(5)
        self.driver.find_element_by_name('login_password').send_keys(self.password)

        submit = self.driver.find_element_by_id('login_submit')
        submit.click()

        if self.notify:
            msg = "Login erfolgreich"
            self.notify.send(msg)

    def updAnzeige(self,id):
        self.driver.get(self.url + "/angebot-bearbeiten.html?action=update_offer&offer_id=" + str(id))
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'update_offer')))
        submit = self.driver.find_element_by_id('update_offer_nav')
        submit.click()

        if self.notify:
            msg = "Anzeige "+id+" wurde aktualisiert!\n"+self.url+"/"+id+".html"
            self.notify.send(msg)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-U', '--username', help='Username or your email of your account', action='store',required=True)
    parser.add_argument('-P', '--password', help='Password of your account', action='store', required=True)
    #parser.add_argument('-u', '--url', help='Login URL', action='store', required=True)
    args = parser.parse_args()
    notify = telegramNotify.notify("661434768:AAFEjE-FgNiGB7gxUxBROgvD8oLMXAXM1Lg","190037850")

    try:
        with webInterface(args.username, args.password, notify) as pv:
            pv.login()
            time.sleep(5)
            pv.updAnzeige("8225189")
            time.sleep(30)
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()
