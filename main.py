from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QDesktopServices
import datetime
import requests
import glob
import os
import traceback
from threading import Thread
import shutil
import time
import hashlib
import pandas as pd
from pathlib import Path
import numpy as np
import base64
import ctypes, sys
import sys
from PyQt5.QtWidgets import *
import zipfile
import io
from Cryptodome.Cipher import AES
from Cryptodome import Cipher
from tkinter import filedialog as fd
import subprocess
import hashlib
import math
import decrypt_pack
import encrypt_pack
import csv
import helper
from helper import *

output_path = "game_files"
lists_paths = "decrypted_lists"
form_class = uic.loadUiType("libs\\firstmenu.ui")[0]
form_class2 = uic.loadUiType("libs\\uniteditdialog.ui")[0]
form_class3 = uic.loadUiType("libs\\otherseditdialog.ui")[0]
#pyinstaller -F -w -i "icon.ico" --add-data="C:\bcmodmaker\bcmodmaker\decrypt_pack.py;decrypt_pack.py" --add-data="C:\bcmodmaker\bcmodmaker\encrypt_pack.py;encrypt_pack.py" --add-data="C:\bcmodmaker\bcmodmaker\helper.py;helper.py" main.py


def zip_folder(folder_path, zip_path):
    # Create a ZIP file object
    zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)

    # Iterate over all the files and folders in the specified folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            # Get the full path of the file
            file_path = os.path.join(root, file)
            
            # Calculate the relative path inside the ZIP file
            relative_path = os.path.relpath(file_path, folder_path)
            
            # Add the file to the ZIP file with its relative path
            zipf.write(file_path, relative_path)

    # Close the ZIP file
    zipf.close()

def TSVEdit(filename: str, row_index: int, column_index: int, new_value: str):
        
    with open(filename, 'r', newline='') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        rows = list(reader)

    rows[row_index][column_index] = new_value

    with open(filename, 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        writer.writerows(rows)

def TSVRead(filename: str, row_index: int, column_index: int):
        
    with open(filename, 'r', newline='') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        rows = list(reader)
        return str(rows[row_index][column_index])
    


class WindowClass3(QMainWindow, form_class3) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('libs\\icon.png'))
        self.itemshopset()
        self.itemshopapply.clicked.connect(self.itemshopupdate)
        
    def itemshopset(self):
        self.itemshoptable.setItem(0, 0, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 1, 3)))
        self.itemshoptable.setItem(1, 0, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 2, 3)))
        self.itemshoptable.setItem(2, 0, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 3, 3)))
        self.itemshoptable.setItem(3, 0, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 4, 3)))
        self.itemshoptable.setItem(4, 0, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 5, 3)))
        self.itemshoptable.setItem(5, 0, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 6, 3)))
        self.itemshoptable.setItem(6, 0, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 7, 3)))
        self.itemshoptable.setItem(7, 0, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 8, 3)))
        self.itemshoptable.setItem(8, 0, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 9, 3)))
        self.itemshoptable.setItem(9, 0, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 10, 3)))
        self.itemshoptable.setItem(10, 0, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 11, 3)))
        self.itemshoptable.setItem(11, 0, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 12, 3)))
        self.itemshoptable.setItem(12, 0, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 13, 3)))
        self.itemshoptable.setItem(13, 0, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 14, 3)))
        self.itemshoptable.setItem(0, 1, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 1, 2)))
        self.itemshoptable.setItem(1, 1, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 2, 2)))
        self.itemshoptable.setItem(2, 1, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 3, 2)))
        self.itemshoptable.setItem(3, 1, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 4, 2)))
        self.itemshoptable.setItem(4, 1, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 5, 2)))
        self.itemshoptable.setItem(5, 1, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 6, 2)))
        self.itemshoptable.setItem(6, 1, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 7, 2)))
        self.itemshoptable.setItem(7, 1, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 8, 2)))
        self.itemshoptable.setItem(8, 1, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 9, 2)))
        self.itemshoptable.setItem(9, 1, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 10, 2)))
        self.itemshoptable.setItem(10, 1, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 11, 2)))
        self.itemshoptable.setItem(11, 1, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 12, 2)))
        self.itemshoptable.setItem(12, 1, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 13, 2)))
        self.itemshoptable.setItem(13, 1, QTableWidgetItem(TSVRead("game_files\\DataLocal\\itemShopData.tsv", 14, 2)))

    def itemshopupdate(self):
        data = self.itemshoptable.item(0, 0).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 1, 3, data)
        data = self.itemshoptable.item(1, 0).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 2, 3, data)
        data = self.itemshoptable.item(2, 0).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 3, 3, data)
        data = self.itemshoptable.item(3, 0).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 4, 3, data)
        data = self.itemshoptable.item(4, 0).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 5, 3, data)
        data = self.itemshoptable.item(5, 0).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 6, 3, data)
        data = self.itemshoptable.item(6, 0).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 7, 3, data)
        data = self.itemshoptable.item(7, 0).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 8, 3, data)
        data = self.itemshoptable.item(8, 0).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 9, 3, data)
        data = self.itemshoptable.item(9, 0).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 10, 3, data)
        data = self.itemshoptable.item(10, 0).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 11, 3, data)
        data = self.itemshoptable.item(11, 0).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 12, 3, data)
        data = self.itemshoptable.item(12, 0).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 13, 3, data)
        data = self.itemshoptable.item(13, 0).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 14, 3, data)
        
        data = self.itemshoptable.item(0, 1).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 1, 2, data)
        data = self.itemshoptable.item(1, 1).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 2, 2, data)
        data = self.itemshoptable.item(2, 1).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 3, 2, data)
        data = self.itemshoptable.item(3, 1).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 4, 2, data)
        data = self.itemshoptable.item(4, 1).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 5, 2, data)
        data = self.itemshoptable.item(5, 1).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 6, 2, data)
        data = self.itemshoptable.item(6, 1).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 7, 2, data)
        data = self.itemshoptable.item(7, 1).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 8, 2, data)
        data = self.itemshoptable.item(8, 1).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 9, 2, data)
        data = self.itemshoptable.item(9, 1).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 10, 2, data)
        data = self.itemshoptable.item(10, 1).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 11, 2, data)
        data = self.itemshoptable.item(11, 1).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 12, 2, data)
        data = self.itemshoptable.item(12, 1).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 13, 2, data)
        data = self.itemshoptable.item(13, 1).text()
        TSVEdit("game_files\\DataLocal\\itemShopData.tsv", 14, 2, data)
        QMessageBox.information(self, '성공', '성공적으로 TSV 파일에 적용하였습니다. 변경된 파일의 이름은 다음과 같습니다.\n컴파일시 필요하니 메모해주세요.\n\n[game_files\\DataLocal\\itemShopData.tsv]',
                                        QMessageBox.Ok)

    

class WindowClass(QMainWindow, form_class2) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('libs\\icon.png'))
        self.findunitid.clicked.connect(self.FindUnitSite)
        self.unitloadbtn.clicked.connect(self.UnitLoad)
        self.gachapercenthelp.clicked.connect(self.GachaPercentHelpConnect)
        self.applybutton.clicked.connect(self.ApplySettingsConnect)

    def FindUnitSite(self):
        url = QUrl("https://battle-cats.fandom.com/wiki/Cat_Release_Order")
        QDesktopServices.openUrl(url)

    def ApplySettingsConnect(self):
        reply = QMessageBox.question(self, '변경사항 적용', '변경사항을 모두 적용하시겠습니까?\n게임 손상 / 또는 법적 조치에 대해 책임지지 않습니다.',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        result = str(int(self.unitnumline.text()) + 1).zfill(3)
        
        filename = 'game_files\\DataLocal\\unitbuy.csv'

        with open(filename, 'r') as csvfile:
            lines = csvfile.readlines()
            if "" in lines[-1]:
                
                lines = lines[:-1]

                with open(filename, 'w') as csvfile:
                    csvfile.writelines(lines)

        df_ub = pd.read_csv("game_files\\DataLocal\\unitbuy.csv", sep = ",", encoding = "utf-8", header=None)
        df_ub.iloc[int(result)-1, 2] = int(str(self.unitlevelupxp.text()))
        df_ub.iloc[int(result)-1, 3] = int(str(self.unitlevelupxp.text()))
        df_ub.iloc[int(result)-1, 4] = int(str(self.unitlevelupxp.text()))
        df_ub.iloc[int(result)-1, 5] = int(str(self.unitlevelupxp.text()))
        df_ub.iloc[int(result)-1, 6] = int(str(self.unitlevelupxp.text()))
        df_ub.iloc[int(result)-1, 7] = int(str(self.unitlevelupxp.text()))
        df_ub.iloc[int(result)-1, 8] = int(str(self.unitlevelupxp.text()))
        df_ub.iloc[int(result)-1, 9] = int(str(self.unitlevelupxp.text()))
        df_ub.iloc[int(result)-1, 10] = int(str(self.unitlevelupxp.text()))
        df_ub.iloc[int(result)-1, 11] = int(str(self.unitlevelupxp.text()))
        df_ub.iloc[int(result)-1, 50] = int(str(self.unitleveluplimit.text()))
        df_ub.iloc[int(result)-1, 51] = int(str(self.unitplusleveluplimit.text()))
        df_ub.iloc[int(result)-1, 13] = int(str(self.unitgachararity.text()))
        df_ub.to_csv("game_files\\DataLocal\\unitbuy.csv", index=False, header=None)

        


        df = pd.read_csv("game_files\\DataLocal\\unit{}.csv".format(result), sep = ",", encoding = "utf-8", header=None)
        df.iloc[0, 0] = int(str(self.healthinput.text()))
        df.iloc[0, 1] = int(str(self.knockbackinput.text()))
        df.iloc[0, 2] = int(str(self.movespeedinput.text()))
        df.iloc[0, 3] = int(str(self.attackpowerinput.text()))
        df.iloc[0, 4] = int(str(self.attackcooltimeinput.text()))
        df.iloc[0, 6] = int(str(self.gocostinput.text()))
        df.iloc[0, 7] = int(str(self.gocooltimeinput.text()))

        
        df.to_csv("game_files\\DataLocal\\unit{}.csv".format(result), index=False, header=None)
        QMessageBox.information(self, '성공', '성공적으로 CSV 파일에 적용하였습니다. 변경된 파일의 이름은 다음과 같습니다.\n컴파일시 필요하니 메모해주세요.\n\n[game_files\\DataLocal\\unit{}.csv, game_files\\DataLocal\\unitbuy.csv]'.format(result),
                                        QMessageBox.Ok)


    def UnitLoad(self):
        result = str(int(self.unitnumline.text()) + 1).zfill(3)

        df_ub = pd.read_csv("game_files\\DataLocal\\unitbuy.csv", sep = ",", encoding = "utf-8", header=None)
        self.unitlevelupxp.setText(str(int(df_ub.iloc[int(result)-1 , 2])))
        self.unitleveluplimit.setText(str(int(df_ub.iloc[int(result)-1 , 50])))
        self.unitplusleveluplimit.setText(str(int(df_ub.iloc[int(result)-1 , 51])))
        self.unitgachararity.setText(str(int(df_ub.iloc[int(result)-1 , 13])))


        df = pd.read_csv("game_files\\DataLocal\\unit{}.csv".format(result), sep = ",", encoding = "utf-8", header=None)
        self.healthinput.setText(str(int(df.iloc[0, 0])))
        self.knockbackinput.setText(str(int(df.iloc[0, 1])))
        self.movespeedinput.setText(str(int(df.iloc[0, 2])))
        self.attackpowerinput.setText(str(int(df.iloc[0, 3])))
        self.attackcooltimeinput.setText(str(int(df.iloc[0, 4])))
        self.gocostinput.setText(str(int(df.iloc[0, 6])))
        self.gocooltimeinput.setText(str(int(df.iloc[0, 7])))
        
        



    def GachaPercentHelpConnect(self):
        QMessageBox.information(self, '도움말', '이 설정값은 레어등급별 뽑기확률을 설정합니다.\n\n0: 뽑기에서 출현하지 않음\n1: EX 확률로 출현\n2: 레어 확률로 출현\n3: 슈퍼 레어 확률로 출현\n4: 울슈레 확률로 출현\n5: 레전드 레어 확률로 출현',
                                        QMessageBox.Ok)
    



class WindowClass2(QMainWindow, form_class):
    def __init__(self) :
        listfile1 = pd.read_csv(io.StringIO(requests.get("https://github.com/cintagram/bcmodmaker_assets/raw/main/apklist.csv").text), sep = ",", encoding = "utf-8")
        listfile = listfile1.loc[listfile1["apptype"] == "ipa", "name"].values
        listfile2 = listfile1.loc[listfile1["apptype"] == "apk", "name"].values
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('libs\\icon.png'))
        self.ipadownloadbtn.clicked.connect(self.download_ipa)
        self.apkdownloadbtn.clicked.connect(self.download_apk)
        self.makeipa.clicked.connect(self.make_ipa)
        self.makeapk.clicked.connect(self.make_apk)
        i = 0
        for i in range(len(listfile)):
            self.ipaselector.addItem("{}".format(listfile[i]))
            i += 1
        j = 0
        for j in range(len(listfile2)):
            self.apkselector.addItem("{}".format(listfile2[j]))
            j += 1
        self.ipadecompilebtn.clicked.connect(self.extract_ipa)
        self.apkdecompilebtn.clicked.connect(self.extract_apk)
        self.decompilebtn.clicked.connect(self.decrypt_pack_ui)
        self.compilebtn.clicked.connect(self.encrypt_pack_ui)
        self.catseditorbtn.clicked.connect(self.CatsEditorConnect)
        self.otherseditorbtn.clicked.connect(self.OthersEditorConnect)
        if not os.path.exists("game_files\\DataLocal"):
            self.catseditorbtn.setDisabled(True)
            self.enemyeditorbtn.setDisabled(True)
            self.stageeditorbtn.setDisabled(True)
            self.otherseditorbtn.setDisabled(True)
        else:
            self.catseditorbtn.setDisabled(False)
            self.enemyeditorbtn.setDisabled(True)
            self.stageeditorbtn.setDisabled(True)
            self.otherseditorbtn.setDisabled(False)
        
        current_version = "1.0 beta"
        server_version = requests.get("https://github.com/cintagram/bcmodmaker_assets/raw/main/version.txt").text
        message = requests.get("https://github.com/cintagram/bcmodmaker_assets/raw/main/message.txt").text
        print(server_version)
        if not current_version in server_version:
            QMessageBox.warning(self, 'New Update', '업데이트 알림\n{}'.format(message),
                                        QMessageBox.Ok)
            sys.exit(1)
        elif current_version == server_version:
            if message == 'None':
                QMessageBox.information(self, '주의!', '이버전은 베타버전이므로, 제대로 적용되지 않거나 버그가 있을 수 있습니다.',
                                            QMessageBox.Ok)
                pass
            else:
                QMessageBox.information(self, '개발자의 메시지', '개발자의 메시지\n\n{}'.format(message),
                                            QMessageBox.Ok)
                  
    def add_text(self, text):
        self.logbox.appendPlainText(text)
        
    def download_ipa(self):
        selected = str(self.ipaselector.currentText())
        print(selected)
        QMessageBox.information(self, '다운로드 시작하기', '다운로드를 시작합니다.\n응답없음 상태가 되어도 창을 닫지마세요.\n확인을 누르면 시작합니다.',
                                    QMessageBox.Ok)
        self.progressBar.setValue(20)
        
        df = pd.read_csv(io.StringIO(requests.get("https://github.com/cintagram/bcmodmaker_assets/raw/main/apklist.csv").text), sep = ",", encoding = "utf-8")
        self.add_text("Reading file info from server...")
        country = df.loc[df["name"] == selected, "country"].values[0]
        version = df.loc[df["name"] == selected, "version"].values[0]
        ipa_url = df.loc[df["name"] == str(selected), "link"].values[0]
        self.add_text("Downloading...")
        response = requests.get(ipa_url)
        file = open("jp.co.ponos.battlecats{}_{}.ipa".format(country, version), "wb").write(response.content)
        self.add_text("Completed Downloading")
        self.progressBar.setValue(100)
        QMessageBox.information(self, '성공', '다운로드에 성공하였습니다.\n[jp.co.ponos.battlecats{}_{}.ipa]'.format(country, version),
                                    QMessageBox.Ok)
        self.progressBar.setValue(0)

    def extract_ipa(self):
        pack_paths = helper.select_files(".ipa 파일을 선택해주세요.", [(".ipa", "*.ipa")], False)
        if pack_paths:
            self.add_text("Preparing extraction...")
            self.progressBar.setValue(45)
            p = Path(pack_paths[0])
            fantasy_zip = zipfile.ZipFile(p)
            self.add_text("Extracting...")
            self.progressBar.setValue(70)
            fantasy_zip.extractall()
            fantasy_zip.close()
            self.add_text("Completed Extraction.")
            self.progressBar.setValue(100)
            QMessageBox.information(self, '성공', '다음 폴더에 압축을 풀었습니다: [Payload]\n[Payload\\] 폴더를 확인해주세요.',
                                        QMessageBox.Ok)
            
        
    def download_apk(self):
        selected = str(self.apkselector.currentText())
        print(selected)
        QMessageBox.information(self, '다운로드 시작하기', '다운로드를 시작합니다.\n응답없음 상태가 되어도 창을 닫지마세요.\n확인을 누르면 시작합니다.',
                                    QMessageBox.Ok)
        self.progressBar.setValue(20)
        
        df = pd.read_csv(io.StringIO(requests.get("https://github.com/cintagram/bcmodmaker_assets/raw/main/apklist.csv").text), sep = ",", encoding = "utf-8")
        self.add_text("Reading file info from server...")
        country = df.loc[df["name"] == selected, "country"].values[0]
        version = df.loc[df["name"] == selected, "version"].values[0]
        apk_url = df.loc[df["name"] == str(selected), "link"].values[0]
        self.add_text("Downloading...")
        response = requests.get(apk_url)
        file = open("jp.co.ponos.battlecats{}_{}.apk".format(country, version), "wb").write(response.content)
        self.add_text("Completed Downloading")
        self.progressBar.setValue(100)
        QMessageBox.information(self, '성공', '다운로드에 성공하였습니다.\n[jp.co.ponos.battlecats{}_{}.apk]'.format(country, version),
                                    QMessageBox.Ok)
        self.progressBar.setValue(0)

    def extract_apk(self):
        QMessageBox.information(self, '안내', '동봉된 툴인 APKToolGUI를 실행하여, Decompile 버튼 옆 ... 버튼을 눌러 APK를 선택 후, 디컴파일해주세요.',
                                        QMessageBox.Ok)

    def decrypt_pack_ui(self):
        self.add_text("Initialized directories.")
        country_code, ok = QInputDialog.getText(self, '국가 입력', '국가 코드를 입력해주세요.\n\n한국판: kr\n영미/글로벌판: en\n일본판: jp')
        if ok:
            self.add_text("Country: {}".format(country_code))
            QMessageBox.information(self, '파일 선택 가이드', '파일 선택 창이 뜨면 다음 2개의 파일들을 반드시 선택해주세요. 나머지는 선택입니다.\n\nDataLocal.pack\nDownloadLocal.pack',
                                    QMessageBox.Ok)
            if country_code == "jp":
                jp = True
            elif country_code == "en" or country_code == "kr":
                jp = False


            decrypt_pack.decrypt(jp, country_code)


            self.add_text("Completed Decryption.")
            self.progressBar.setValue(100)
            QMessageBox.information(self, '디컴파일 성공', '파일들을 모두 디컴파일 완료했습니다.\n\n다음 폴더에 파일들을 저장했습니다. [game_files]',
                                QMessageBox.Ok)
            self.progressBar.setValue(0)
            if not os.path.exists("game_files\\DataLocal"):
                self.catseditorbtn.setDisabled(True)
                self.enemyeditorbtn.setDisabled(True)
                self.stageeditorbtn.setDisabled(True)
                self.otherseditorbtn.setDisabled(True)
            else:
                self.catseditorbtn.setDisabled(False)
                self.enemyeditorbtn.setDisabled(True)
                self.stageeditorbtn.setDisabled(True)
                self.otherseditorbtn.setDisabled(True)

    def encrypt_pack_ui(self):
        initial_dir = "game_files"
        output_path = "encrypted_files"
        downloadlocal = "game_files\\DownloadLocal"
        datalocal = "game_files\\DataLocal"
        self.add_text("Initialized directories.")
        country_code, ok = QInputDialog.getText(self, '국가 입력', '국가 코드를 입력해주세요.\n\n한국판: kr\n영미/글로벌판: en\n일본판: jp')
        if ok:
            if country_code == "jp":
                jp = True
            elif country_code == "en" or country_code == "kr":
                jp = False
                

            encrypt_pack.encrypt(jp, country_code)
            self.add_text("Completed Encryption.")
            self.progressBar.setValue(100)
            QMessageBox.information(self, '성공', '파일들을 모두 컴파일 완료했습니다.\n\n다음 폴더에 파일들을 저장했습니다. [encrypted_files]',
                                QMessageBox.Ok)
            self.progressBar.setValue(0)
        
    def make_ipa(self):
        initial_dir = ""
        country_code, ok = QInputDialog.getText(self, '국가 입력', '국가 코드를 입력해주세요.\n\n한국판: kr\n영미/글로벌판: en\n일본판: jp')
        
        if ok:
            if country_code == "jp":
                county_code = ""
            pack_paths = select_dir("Payload 폴더를 선택해주세요.", initial_dir)
            if pack_paths:
                source_file1 = 'encrypted_files\\DownloadLocal.list'
                source_file2 = 'encrypted_files\\DownloadLocal.pack'
                destination_directory = os.path.join(pack_paths, "battlecats{}.app\\".format(country_code))
                shutil.copy(source_file1, destination_directory)
                shutil.copy(source_file2, destination_directory)
                self.add_text("Preparing Zip...")
                self.progressBar.setValue(45)
                folder_path = destination_directory
                zip_path = 'jp.co.ponos.battlecats{}_MOD_Pulservice.ipa'.format(country_code)
                self.add_text("Compressing and Converting...")
                zip_folder(folder_path, zip_path)
                self.add_text("Completed Compression.")
                self.progressBar.setValue(100)
                QMessageBox.information(self, '성공', '현재 폴더에 앱 파일을 생성하였습니다.\n\n{}'.format(zip_path),
                                            QMessageBox.Ok)
                self.progressBar.setValue(0)

    def make_apk(self):
        QMessageBox.information(self, '안내', '1. encrypted_files 폴더 안의 [DownloadLocal.pack, DownloadLocal.list] 파일 2개를 apk폴더 속의 assets 폴더 속에 덮어씌워주세요.\n\n2. 동봉된 툴인 APKToolGUI를 실행하여, Compile 버튼 옆 ... 버튼을 눌러 폴더를 선택 후, 컴파일해주세요.',
                                        QMessageBox.Ok)


    def CatsEditorConnect(self):
        self.w = WindowClass()
        self.w.show()
    
    def OthersEditorConnect(self):
        self.w = WindowClass3()
        self.w.show()
    


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    myWindow = WindowClass2() 
    myWindow.show()
    app.exec_()