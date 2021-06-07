#!/home/jaybraker/venvs/wggesucht/venv/bin/python3
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
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
        self.url: str = "https://www.motherless.com"
        self.notify = notify
        chromeOptions = Options()
        chromeOptions.headless = True
        self.driver = webdriver.Chrome('/home/jaybraker/venvs/selenium/chromedriver', options=chromeOptions)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    def login(self):
        self.driver.get(self.url + "/login")

        time.sleep(2)
        self.driver.find_element_by_id('form-username').send_keys(self.username)
        time.sleep(1)
        self.driver.find_element_by_id('form-password').send_keys(self.password)

        submit = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/div/div[1]/form/div/div/div[5]/div/button')
        submit.click()

        if self.notify:
            msg = "Login erfolgreich"
            print(msg)
            #self.notify.send(msg)

    def checkMsgs(self):
        msgs = []
        self.driver.get(self.url + "/mail")

        time.sleep(3)
        message_entries = self.driver.find_element_by_class_name("mail-rows")
        unread = message_entries.find_elements_by_class_name("mail-status-unread")
        for e in unread:
            msg = e.find_element_by_tag_name('a').get_attribute('href')
            msgs.append(str(msg))

        if self.notify:
            if len(msgs) > 0:
                txt = "You've got: " + str(len(msgs)) + " messages"
                self.notify.send(txt)
        return msgs

    def getMsgs(self, msgs):
        for e in msgs:
            msg = {}
            self.driver.get(e)
            time.sleep(2)
            txt = self.driver.find_element_by_class_name('message_body')
            try:
                quote = txt.find_element_by_tag_name('blockquote').text
            except: quote = ""
            sender = self.driver.find_element_by_class_name('message-header-from')

            msg['text'] = str(txt.text.replace(quote,'').replace('\n',''))
            msg['sender'] = str(sender.text)
            msg['sender_url'] = str(sender.find_element_by_tag_name('a').get_attribute('href'))
            msg['sent'] = str(self.driver.find_element_by_class_name('message-header-date').text)
            msg['last_seen'] = str(self.getLastSeen(msg['sender_url']))

            if self.notify:
                txt = "From: " + msg['sender'] + " " + msg['last_seen'] + "\n" + msg['sent'] + "\n" +  msg['text']
                self.notify.send(txt)

    def getLastSeen(self,url):
        self.driver.get(url)

        time.sleep(3)
        stats = self.driver.find_elements_by_class_name('profile-stats')
        for e in stats:
            if e.find_element_by_tag_name('span').text == 'Last Seen:':
                return e.text
        return None

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
            time.sleep(3)
            msgs = pv.checkMsgs()
            if msgs: pv.getMsgs(msgs)
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()
