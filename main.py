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

output_path = "game_files"
lists_paths = "decrypted_lists"
form_class = uic.loadUiType("libs\\firstmenu.ui")[0]
form_class2 = uic.loadUiType("libs\\uniteditdialog.ui")[0]

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

def insert_list(main, list, index):
    for i in range(len(list)):
        main[index+i] = list[i]
    return main

def encrypt_file(file_data, jp, pk_name, country_code):
    aes_mode = AES.MODE_CBC
    if jp:
        key = bytes.fromhex("d754868de89d717fa9e7b06da45ae9e3")
        iv = bytes.fromhex("40b2131a9f388ad4e5002a98118f6128")
    elif country_code == "en":
        key = bytes.fromhex("0ad39e4aeaf55aa717feb1825edef521")
        iv = bytes.fromhex("d1d7e708091941d90cdf8aa5f30bb0c2")
    elif country_code == "kr":
        key = bytes.fromhex("bea585eb993216ef4dcb88b625c3df98")
        iv = bytes.fromhex("9b13c2121d39f1353a125fed98696649")
    
    
    if "server" in pk_name.lower():
        key = md5_str("battlecats")
        iv = None
        aes_mode = AES.MODE_ECB
    if iv:
        cipher = AES.new(key, aes_mode, iv)
    else:
        cipher = AES.new(key, aes_mode)
    encrypted_data = cipher.encrypt(file_data)
    return encrypted_data

def encrypt_list(list_data):
    key = md5_str("pack")
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(list_data)
    return encrypted_data

def create_pack(game_files_dir, ls_data, jp, pk_name, country_code):
    split_data = parse_csv_file(None, ls_data.split("\n"), 3)
    pack_data = [0] * (int(split_data[-1][1]) + int(split_data[-1][2]))
    
    for i in range(len(split_data)):
        file = split_data[i]

        name = file[0]
        start_offset = int(file[1])

        file_data = open_file_b(os.path.join(game_files_dir, name))
        if "imagedatalocal" in pk_name.lower():
            encrypted_data = file_data
        else:
            encrypted_data = encrypt_file(file_data, jp, pk_name, country_code)
        encrypted_data = list(encrypted_data)
        pack_data = insert_list(pack_data, encrypted_data, start_offset)
        
    return pack_data

def select_dir(title, initial_dir):
    path = fd.askdirectory(title=title, initialdir=initial_dir)
    return path

def str_to_gv(game_version: str):
        split_gv = game_version.split(".")
        if len(split_gv) == 2:
            split_gv.append("0")
        final = ""
        for split in split_gv:
            final += split.zfill(2)

        return final.lstrip("0")

def find_lists(pack_paths):
    files = []
    for pack_path in pack_paths:
        directory = os.path.dirname(pack_path)
        ls_path = os.path.join(directory, pack_path.rstrip(".pack") + ".list")
        group = {"pack" : pack_path, "list" : ls_path}
        files.append(group)
    return files

def add_extra_bytes(path, overwrite=True, data=None, extra=False):
    if not data:
        data = open_file_b(path)
    data = list(data)
    rem = math.ceil(len(data) / 16)
    rem *= 16
    rem -= len(data)
    
    if rem != 16:
        for i in range(rem):
            data.append(rem)
    data = bytes(data)
    if overwrite:
        write_file_b(path, data)
    if extra:
        return rem
    else:
        return data

def filter_list(data : list, black_list : list):
    trimmed_data = data
    for i in range(len(data)):
        item = data[i]
        for banned in black_list:
            if banned in item:
                index = item.index(banned)
                item = item[:index]
                trimmed_data[i] = item
    return trimmed_data

def create_list_decrypt(list, index=True, extra_values=None, offset=None, color=True):
    output = ""
    for i in range(len(list)):
        if index:
            output += f"{i+1}. &{list[i]}&"
        else:
            output += str(list[i])
        if extra_values:
            if offset != None:
                output += f" &:& {extra_values[i]+offset}"
            else:
                output += f" &:& {extra_values[i]}"
        output += "\n"
    output = output.removesuffix("\n")

def create_list_encrypt(game_files_dir):
    #return open("decrypted_lists/DataLocal.list", "r").read()
    list_of_files = glob.glob(game_files_dir + '/*')
    files_with_size = [(file_path, os.stat(file_path).st_size) 
                    for file_path in list_of_files ]
    files = files_with_size
    list_file = f"{len(files_with_size)}\n"
    address = 0
    for i in range(len(files_with_size)):
        file = files_with_size[i]
        if file[1] % 16 != 0:
            extra = add_extra_bytes(file[0], extra=True)
            file = (file[0], file[1] + extra)
            files[i] = file
        
        list_file += f"{os.path.basename(file[0])},{address},{file[1]}\n"
        address += file[1]
    return list_file

def parse_csv_file(path, lines=None, min_length=0, black_list=None):
    if not lines:
        lines = open(path, "r", encoding="utf-8").readlines()
    data = []
    for line in lines:
        line_data = line.split(",")
        if len(line_data) < min_length:
            continue
        if black_list:
            line_data = filter_list(line_data, black_list)

        data.append(line_data)
    return data

def write_csv_file(path, data):
    final = ""
    for row in data:
        for item in row:
            final += f"{item},"
        final += "\n"
    write_file_b(path, final.encode("utf-8"))
    add_extra_bytes(path)

def write_file_b(path, data):
    open(path, "wb").write(data)

def unpack_pack(pk_file_path, ls_data, jp, base_path, country_code):
    list_data = ls_data.decode("utf-8")
    split_data = parse_csv_file(None, list_data.split("\n"), 3)

    pack_data = open_file_b(pk_file_path)

    
    for i in range(len(split_data)):
        file = split_data[i]
        
        name = file[0]
        start_offset = int(file[1])
        length = int(file[2])

        pk_chunk = pack_data[start_offset:start_offset+length]
        base_name = os.path.basename(pk_file_path)
        if "imagedatalocal" in base_name.lower():
            pk_chunk_decrypted = pk_chunk
        else:
            pk_chunk_decrypted = decrypt_pack(pk_chunk, jp, base_name, country_code)
        write_file_b(os.path.join(base_path, name), pk_chunk_decrypted)
        
def open_file_b(path):
    f = open(path, "rb").read()
    return f

def unpack_list(ls_file):
    data = open_file_b(ls_file)
    key = md5_str("pack")
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(data)
    return decrypted_data

def md5_str(string, length=8):
    return bytearray(hashlib.md5(string.encode("utf-8")).digest()[:length]).hex().encode("utf-8")

def decrypt_pack(chunk_data, jp, pk_name, country_code):
    aes_mode = AES.MODE_CBC
    if jp:
        key = bytes.fromhex("d754868de89d717fa9e7b06da45ae9e3")
        iv = bytes.fromhex("40b2131a9f388ad4e5002a98118f6128")
    elif country_code == "en":
        key = bytes.fromhex("0ad39e4aeaf55aa717feb1825edef521")
        iv = bytes.fromhex("d1d7e708091941d90cdf8aa5f30bb0c2")
    
    elif country_code == "kr":
        key = bytes.fromhex("bea585eb993216ef4dcb88b625c3df98")
        iv = bytes.fromhex("9b13c2121d39f1353a125fed98696649")
    
    if "server" in pk_name.lower():
        key = md5_str("battlecats")
        iv = None
        aes_mode = AES.MODE_ECB
    if iv:
        cipher = AES.new(key, aes_mode, iv)
    else:
        cipher = AES.new(key, aes_mode)
    decrypted_data = cipher.decrypt(chunk_data)
    return decrypted_data

def validate_bool(string, true="y"):
    string = string.strip(" ")

    if string.lower() == true:
        return True
    else:
        return False

def ls_to_str(list):
    val = ""
    for item in list:
        val += item
    return val

def str_to_ls(str):
    ls = []
    for char in str:
        ls.append(char)
    return ls

def check_and_create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def select_files(title, file_types, single=True, default=""):
    if single:
        path = fd.askopenfilename(title=title, filetypes=file_types, initialdir=default)
    else:
        path = fd.askopenfilenames(title=title, filetypes=file_types, initialdir=default)
    return path

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
        df = pd.read_csv("game_files\\DataLocal\\unit{}.csv".format(result), sep = ",", encoding = "utf-8", header=None)
        df.iloc[0, 0] = int(str(self.healthinput.text()))
        df.iloc[0, 1] = int(str(self.knockbackinput.text()))
        df.iloc[0, 2] = int(str(self.movespeedinput.text()))
        df.iloc[0, 3] = int(str(self.attackpowerinput.text()))
        df.iloc[0, 4] = int(str(self.attackcooltimeinput.text()))
        df.iloc[0, 6] = int(str(self.gocostinput.text()))
        
        df.to_csv("game_files\\DataLocal\\unit{}.csv".format(result), index=False, header=None)
        QMessageBox.information(self, '성공', '성공적으로 CSV 파일에 적용하였습니다. 변경된 파일의 이름은 다음과 같습니다.\n컴파일시 필요하니 메모해주세요.\n\n[game_files\\DataLocal\\unit{}.csv]'.format(result),
                                        QMessageBox.Ok)


    def UnitLoad(self):
        result = str(int(self.unitnumline.text()) + 1).zfill(3)
        df = pd.read_csv("game_files\\DataLocal\\unit{}.csv".format(result), sep = ",", encoding = "utf-8", header=None)
        self.healthinput.setText(str(int(df.iloc[0, 0])))
        self.knockbackinput.setText(str(int(df.iloc[0, 1])))
        self.movespeedinput.setText(str(int(df.iloc[0, 2])))
        self.attackpowerinput.setText(str(int(df.iloc[0, 3])))
        self.attackcooltimeinput.setText(str(int(df.iloc[0, 4])))
        self.gocostinput.setText(str(int(df.iloc[0, 6])))



    def GachaPercentHelpConnect(self):
        QMessageBox.information(self, '도움말', '이 설정값은 레어등급별 뽑기확률을 설정합니다.\n\n0: 뽑기에서 출현하지 않음\n1: 레어 확률로 출현\n2: 슈퍼 레어 확률로 출현\n3: 울슈레 확률로 출현\n4: 레전드 레어 확률로 출현',
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
        pack_paths = select_files(".ipa 파일을 선택해주세요.", [(".ipa", "*.ipa")], False)
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
            pack_paths = select_files(".pack 파일을 선택해주세요.", [(".pack", "*.pack")], False)
            if pack_paths:
                QMessageBox.information(self, '디컴파일 시작하기', '디컴파일을 시작합니다.\n응답없음 상태가 되어도 창을 닫지마세요.\n확인을 누르면 시작합니다.',
                                    QMessageBox.Ok)
                if country_code == "jp":
                    jp = "y"
                else:
                    jp = "n"
                jp = validate_bool(jp)
                check_and_create_dir("game_files")
                file_groups = find_lists(pack_paths)
                self.add_text("Finding lists for game files...")
                self.progressBar.setValue(45)
                for i in range(len(file_groups)):
                    file_group = file_groups[i]

                    ls_base_name = os.path.basename(file_group["list"])
                    pk_base_name = os.path.basename(file_group["pack"])

                    name = pk_base_name.rstrip(".pack")
                    path = os.path.join(output_path, name)

                    check_and_create_dir(path)
                    check_and_create_dir(lists_paths)

                    ls_data = unpack_list(file_group["list"])
                    write_file_b(os.path.join(lists_paths, ls_base_name), ls_data)
                    self.add_text("Writing bytes for decryption...")
                    
                    unpack_pack(file_group["pack"], ls_data, jp, path, country_code)
                self.add_text("Completed Decryption.")
                self.progressBar.setValue(100)
                QMessageBox.information(self, '디컴파일 성공', '다음 파일들을 모두 디컴파일 완료했습니다.\n{}\n\n다음 폴더에 파일들을 저장했습니다. [game_files]'.format(pack_paths),
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
            name, ok = QInputDialog.getText(self, '폴더 이름 입력', '컴파일될 파일의 이름 (폴더의 이름)을 입력해주세요.\n\n예시: DownloadLocal / DataLocal')
            if ok:
                self.add_text("Country: {}".format(country_code))
                QMessageBox.information(self, '파일 선택 가이드', '파일 선택 창이 뜨면 다음 2개의 파일들을 반드시 선택해주세요.\n\nDownloadLocal.pack',
                                        QMessageBox.Ok)
                game_files_dir = select_dir("Select a folder of game files", initial_dir)
                if game_files_dir:
                    QMessageBox.warning(self, '컴파일 작업', '수정하신 모든 파일들을 DownloadLocal 폴더 속에 붙여넣어주세요.\n안그러면 적용되지 않습니다.',
                                        QMessageBox.Ok)
                    self.progressBar.setValue(20)
                    QMessageBox.information(self, 'PACK 컴파일 시작하기', 'PACK 컴파일을 시작합니다.\n응답없음 상태가 되어도 창을 닫지마세요.\n확인을 누르면 시작합니다.',
                                        QMessageBox.Ok)
                    if country_code == "jp":
                        jp = "y"
                    else:
                        jp = "n"
                    
                    
                    check_and_create_dir(output_path)
                    list_data = create_list_encrypt(game_files_dir)
                    self.progressBar.setValue(47)
                    self.add_text("Creating encryption list...")
                    list_data_full = add_extra_bytes(None, False, list_data.encode("utf-8"))
                    self.add_text("Adding extra bytes...")
                    self.progressBar.setValue(60)
                    encrypted_data_list = encrypt_list(list_data_full)
                    ls_output = os.path.join(output_path, name + ".list")
                    write_file_b(ls_output, encrypted_data_list)
                    self.add_text("Writing bytes..")
                    self.progressBar.setValue(71)
                    pack_data = create_pack(game_files_dir, list_data, jp, name, country_code)
                    pk_output = os.path.join(output_path, name + ".pack")
                    write_file_b(pk_output, bytes(pack_data))
                    self.add_text("Completed Encryption.")
                    self.progressBar.setValue(100)
                    QMessageBox.information(self, '성공', '다음 파일들을 모두 컴파일 완료했습니다.\n{}\n\n다음 폴더에 파일들을 저장했습니다. [encrypted_files]'.format(game_files_dir),
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
    


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    myWindow = WindowClass2() 
    myWindow.show()
    app.exec_()