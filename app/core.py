from selenium import webdriver as driver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from PyQt5.QtCore import QObject, pyqtSignal

class Core(QObject):
    finished =pyqtSignal()
    running = pyqtSignal(bool)

    def __init__(self, email, password, chromedriver_path, meeting_url):
        super(Core, self).__init__()
        self.email=email
        self.password=password
        self.chromedriver_path=chromedriver_path
        self.meeting_url=meeting_url
        self.opt=Options()
        self.opt.add_argument('--disable-blink-features=AutomationControlled')
        self.opt.add_argument('--start-maximized')
        self.opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 0,
            "profile.default_content_setting_values.notifications": 1
        })
        self.service=Service('D:\TOOLS\chromedriver_win32\chromedriver.exe')
        self.driver = driver.Chrome(options=self.opt, service=self.service)


    def LoginGMail(self):
        self.driver.get("https://accounts.google.com/ServiceLogin?hl=id&passive=true")

        self.driver.find_element_by_id("identifierId").send_keys(self.email)
        self.driver.find_element_by_id("identifierNext").click()
        self.driver.implicitly_wait(10)

        self.driver.find_element_by_xpath(
            '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(self.password)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("passwordNext").click()
        self.driver.implicitly_wait(10)

        self.driver.get('https://google.com/')
        self.driver.implicitly_wait(2000)
        time.sleep(3)


    def turnOffMicAndCam(self):
        time.sleep(3)
        self.driver.find_element_by_xpath(
            '//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[3]/div/div/div[1]/div[1]/div/div[4]/div[1]/div/div/div').click()
        self.driver.implicitly_wait(3000)
    
        # turn off camera
        time.sleep(1)
        self.driver.find_element_by_xpath(
            '//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[3]/div/div/div[1]/div[1]/div/div[4]/div[2]/div/div').click()
        self.driver.implicitly_wait(3000)

    def AskToJoin(self):
        time.sleep(5)
        self.driver.implicitly_wait(2000)
        self.driver.find_element_by_css_selector(
            'div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()

    def run(self):
        self.LoginGMail()
        self.driver.get(self.meeting_url)
        self.turnOffMicAndCam()
        self.AskToJoin()
        self.running.emit(True)
        while True:
            try:
                time.sleep(3)
                participant=self.driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[10]/div[3]/div[3]/div/div/div[2]/div/div')
                print(participant.text)
                if(participant.text != ''):
                    if (int(participant.text))<=2:
                        self.driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[10]/div[2]/div/div[7]/span/button').click()
            except Exception:
                break
        self.finished.emit()
        self.driver.quit()