import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.sip import setdeleted
from core import Core

class GMeetAutoLeave(QWidget):
    def __init__(self, parent=None) -> None:
        super(GMeetAutoLeave, self).__init__(parent)
        self.switch_window = pyqtSignal(str)
        # wid = QWidget(self)
        # self.setCentralWidget(wid)
        layout = QVBoxLayout()
        #Label
        self.label_path_chrome_driver=QLabel()
        self.label_path_chrome_driver.setText("Lokasi chromedriver")
        self.label_path_chrome_driver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_path_chrome_driver)
        #Text field
        self.text_field_chrome_path=QTextEdit()
        self.text_field_chrome_path.setMaximumHeight(50)
        self.text_field_chrome_path.setReadOnly(True)
        layout.addWidget(self.text_field_chrome_path)
        # Button chromedriver path
        self.button_find_chrome_driver_path = QPushButton("Cari")
        self.button_find_chrome_driver_path.clicked.connect(self.getPathChromeDriver)
        layout.addWidget(self.button_find_chrome_driver_path)
        
        #=====Layout Form
        layout_email_password=QFormLayout()
        layout_email_password.setVerticalSpacing(0)
        #Label Email
        self.label_email=QLabel()
        self.label_email.setText("Masukkan email")       
        #Text field email
        self.text_field_email=QTextEdit()
        self.text_field_email.setMaximumHeight(50)
        # layout_email_password.addWidget(self.text_field_email)
        layout_email_password.addRow(self.label_email, self.text_field_email)

        #Label password
        self.label_password=QLabel()
        self.label_password.setText("Masukkan password")
        #Text field password
        self.text_field_password=QLineEdit()
        self.text_field_password.setMaximumHeight(50)
        self.text_field_password.setEchoMode(QLineEdit.Password)
        layout_email_password.addRow(self.label_password, self.text_field_password)
        
        
        self.email_password_widget=QWidget()
        self.email_password_widget.setLayout(layout_email_password)
        
        layout.addWidget(self.email_password_widget)
        #Label URL meeting
        self.label_url_meeting=QLabel()
        self.label_url_meeting.setText("Masukkan URL meeting")
        layout.addWidget(self.label_url_meeting)
        #Text field URL meeting
        self.text_field_meeting_url=QTextEdit()
        self.text_field_meeting_url.setMaximumHeight(50)
        layout.addWidget(self.text_field_meeting_url)

        # Button start
        self.button_start=QPushButton("Mulai")
        self.button_start.clicked.connect(self.runAutoLeaveGMeet)
        layout.addWidget(self.button_start)

        #Label running
        self.label_running=QLabel("Belum bergabung dalam Google Meet")
        self.label_running.setStyleSheet("color: red")
        self.label_running.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_running)


        self.setLayout(layout)
        # wid.setLayout(layout)
        self.setWindowTitle("Google Meet Autoleave")
        self.setMinimumWidth(480)
        self.setMinimumHeight(640)
    def getPathChromeDriver(self):
        chromedriver_path=QFileDialog.getOpenFileName(self)
        self.text_field_chrome_path.setText(chromedriver_path[0])

    def runAutoLeaveGMeet(self):
        data={
            "EMAIL": self.text_field_email.toPlainText(),
            "PASSWORD": self.text_field_password.text(),
            "CHROMEDRIVER_PATH": self.text_field_chrome_path.toPlainText(),
            "MEETING_URL": self.text_field_meeting_url.toPlainText()
        }
        self.thread=QThread()
        self.core=Core(email=data["EMAIL"], password=data["PASSWORD"], chromedriver_path=data["CHROMEDRIVER_PATH"], meeting_url=data["MEETING_URL"])
        self.core.moveToThread(self.thread)
        
        self.thread.started.connect(self.core.run)
        self.core.finished.connect(self.thread.quit)
        self.core.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.core.running.connect(self.status)

        self.thread.start()

        self.button_start.setEnabled(False)
        self.button_start.setText("Sedang berjalan")
        
        self.thread.finished.connect(
            lambda: self.button_start.setEnabled(True)
        )

        self.thread.finished.connect(
            lambda: self.reset
        )

    def status(self, running):
        if running==True:
            self.label_running.setText("Sedang dalam pertemuan Google Meet")
            self.label_running.setStyleSheet("color: blue")
    def reset(self):
        self.button_start.setText("Mulai")
        self.label_running.setText("Belum bergabung dalam Google Meet")
        self.label_running.setStyleSheet("color: red")

def run():
    app = QApplication(sys.argv)
    gmeet = GMeetAutoLeave()
    gmeet.show()
    sys.exit(app.exec_())


if __name__=="__main__":
    run()