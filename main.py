from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import datetime
import requests
import os
import traceback
from threading import Thread
import hashlib
import pandas as pd
import base64
import ctypes, sys
import sys
from PyQt5.QtWidgets import *
import io

form_class = uic.loadUiType("firstmenu.ui")[0]

class WindowClass2(QMainWindow, form_class) :
    def __init__(self) :
        listfile1 = pd.read_csv(io.StringIO(requests.get("https://raw.githubusercontent.com/cintagram/bcmodmaker_assets/main/apklist.csv").text), sep = ",", encoding = "utf-8")
        listfile = listfile1["name"]
        #print(listfile)
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))
        self.ipadownloadbtn.clicked.connect(self.download_ipa)
        i = 0
        for i in range(len(listfile)):
            self.ipaselector.addItem("{}".format(listfile[i]))
            i += 1
        """
        current_version = "1.0 beta"
        server_version = requests.get("https://pastebin.com/raw/dhKxZzCR").text
        print(server_version)
        if not current_version == server_version:
            QMessageBox.warning(self, 'New Update', 'New Update is availble.\nPlease download latest version.\nLink: https://discord.gg/NXheRpCUwY',
                                        QMessageBox.Ok)
            sys.exit(1)
        else:
            pass
        """
    def str_to_gv(game_version: str):
        split_gv = game_version.split(".")
        if len(split_gv) == 2:
            split_gv.append("0")
        final = ""
        for split in split_gv:
            final += split.zfill(2)

        return final.lstrip("0")
    
    def download_ipa(self):
        selected = self.ipaselector.currentText()
        QMessageBox.information(self, '다운로드 시작하기', '다운로드를 시작합니다.\n응답없음 상태가 되어도 창을 닫지마세요.\n확인을 누르면 시작합니다.',
                                    QMessageBox.Ok)
        self.progressBar.setValue(20)
        
        df = pd.read_csv(io.StringIO(requests.get("https://raw.githubusercontent.com/cintagram/bcmodmaker_assets/main/apklist.csv").text), sep = ",", encoding = "utf-8")
        appinfo = df.loc[df["name"] == selected, "apptypenversion"]
        country = str(appinfo).split("-")[2]
        version = str(appinfo).split("-")[1]
        ipa_url = df.loc[df["apptypenversion"] == "ipa-{}-{}".format(version, country), "link"]
        response = requests.get(ipa_url)
        file = open("jp.co.ponos.battlecats{}_{}.ipa".format(country, version), "wb").write(response.content)
        self.progressbar.setValue(100)
        QMessageBox.information(self, '성공', '다운로드 성공',
                                    QMessageBox.Ok)
        self.progressbar.setValue(0)

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    myWindow = WindowClass2() 
    myWindow.show()
    app.exec_()