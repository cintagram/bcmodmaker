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
form_class = uic.loadUiType("firstmenu.ui")[0]

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

def create_list(list, index=True, extra_values=None, offset=None, color=True):
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

def create_list(list, index=True, extra_values=None, offset=None, color=True):
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
    if not color:
        output = output.replace("&", "")

def check_and_create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def select_files(title, file_types, single=True, default=""):
    if single:
        path = fd.askopenfilename(title=title, filetypes=file_types, initialdir=default)
    else:
        path = fd.askopenfilenames(title=title, filetypes=file_types, initialdir=default)
    return path

class WindowClass2(QMainWindow, form_class) :
    def __init__(self) :
        listfile1 = pd.read_csv(io.StringIO(requests.get("https://github.com/cintagram/bcmodmaker_assets/raw/main/apklist.csv").text), sep = ",", encoding = "utf-8")
        listfile = listfile1.loc[listfile1["apptype"] == "ipa", "name"].values
        listfile2 = listfile1.loc[listfile1["apptype"] == "apk", "name"].values
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))
        self.ipadownloadbtn.clicked.connect(self.download_ipa)
        i = 0
        for i in range(len(listfile)):
            self.ipaselector.addItem("{}".format(listfile[i]))
            i += 1
        j = 0
        for j in range(len(listfile2)):
            self.apkselector.addItem("{}".format(listfile2[j]))
            j += 1
        self.ipadecompilebtn.clicked.connect(self.extract_ipa)
        self.decompilebtn.clicked.connect(self.decrypt_pack_ui)
        
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
                pass
            else:
                QMessageBox.information(self, '개발자의 메시지', '개발자의 메시지\n\n{}'.format(message),
                                            QMessageBox.Ok)
        
        
    
    def download_ipa(self):
        selected = str(self.ipaselector.currentText())
        print(selected)
        QMessageBox.information(self, '다운로드 시작하기', '다운로드를 시작합니다.\n응답없음 상태가 되어도 창을 닫지마세요.\n확인을 누르면 시작합니다.',
                                    QMessageBox.Ok)
        self.progressBar.setValue(20)
        
        df = pd.read_csv(io.StringIO(requests.get("https://github.com/cintagram/bcmodmaker_assets/raw/main/apklist.csv").text), sep = ",", encoding = "utf-8")
        country = df.loc[df["name"] == selected, "country"].values[0]
        version = df.loc[df["name"] == selected, "version"].values[0]
        ipa_url = df.loc[df["name"] == str(selected), "link"].values[0]
        response = requests.get(ipa_url)
        file = open("jp.co.ponos.battlecats{}_{}.ipa".format(country, version), "wb").write(response.content)
        self.progressBar.setValue(100)
        QMessageBox.information(self, '성공', '다운로드에 성공하였습니다.\n[jp.co.ponos.battlecats{}_{}.ipa]'.format(country, version),
                                    QMessageBox.Ok)
        self.progressBar.setValue(0)

    def extract_ipa(self):
        pack_paths = select_files(".ipa 파일을 선택해주세요.", [(".ipa", "*.ipa")], False)
        if pack_paths:
            self.progressBar.setValue(45)
            p = Path(pack_paths[0])
            fantasy_zip = zipfile.ZipFile(p)
            self.progressBar.setValue(70)
            fantasy_zip.extractall()
            fantasy_zip.close()
            self.progressBar.setValue(100)
            QMessageBox.information(self, '성공', '다음 폴더에 압축을 풀었습니다: [Payload]\n[Payload\\] 폴더를 확인해주세요.',
                                        QMessageBox.Ok)
            self.progressBar.setValue(0)
        
    def download_apk(self):
        selected = str(self.apkselector.currentText())
        print(selected)
        QMessageBox.information(self, '다운로드 시작하기', '다운로드를 시작합니다.\n응답없음 상태가 되어도 창을 닫지마세요.\n확인을 누르면 시작합니다.',
                                    QMessageBox.Ok)
        self.progressBar.setValue(20)
        
        df = pd.read_csv(io.StringIO(requests.get("https://github.com/cintagram/bcmodmaker_assets/raw/main/apklist.csv").text), sep = ",", encoding = "utf-8")
        country = df.loc[df["name"] == selected, "country"].values[0]
        version = df.loc[df["name"] == selected, "version"].values[0]
        apk_url = df.loc[df["name"] == str(selected), "link"].values[0]
        response = requests.get(apk_url)
        file = open("jp.co.ponos.battlecats{}_{}.apk".format(country, version), "wb").write(response.content)
        self.progressBar.setValue(100)
        QMessageBox.information(self, '성공', '다운로드에 성공하였습니다.\n[jp.co.ponos.battlecats{}_{}.apk]'.format(country, version),
                                    QMessageBox.Ok)
        self.progressBar.setValue(0)

    def extract_apk(self):
        pack_paths = select_files(".apk 파일을 선택해주세요.", [(".apk", "*.apk")], False)
        if pack_paths:
            self.progressBar.setValue(45)
            p = Path(pack_paths[0])
            fantasy_zip = zipfile.ZipFile(p)
            self.progressBar.setValue(70)
            fantasy_zip.extractall()
            fantasy_zip.close()
            self.progressBar.setValue(100)
            QMessageBox.information(self, '성공', '현재 폴더에 압축을 풀었습니다',
                                        QMessageBox.Ok)
            self.progressBar.setValue(0)

    def decrypt_pack_ui(self):
        country_code, ok = QInputDialog.getText(self, '국가 입력', '국가 코드를 입력해주세요.\n\n한국판: kr\n영미/글로벌판: en\n일본판: jp')
        if ok:
            QMessageBox.information(self, '파일 선택 가이드', '파일 선택 창이 뜨면 다음 2개의 파일들을 반드시 선택해주세요.\n\nDataLocal.pack\nDownloadLocal.pack\n\n위치: [Payload\\battlecats.app\\]',
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

                    unpack_pack(file_group["pack"], ls_data, jp, path, country_code)
                self.progressBar.setValue(100)
                QMessageBox.information(self, '디컴파일 성공', '다음 파일들을 모두 디컴파일 완료했습니다.\n{}\n\n다음 폴더에 파일들을 저장했습니다. [game_files]'.format(pack_paths),
                                    QMessageBox.Ok)
                self.progressBar.setValue(0)

    def encrypt_pack_ui(self):
        pass   

    def make_ipa(self):
        pass

    def make_apk(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    myWindow = WindowClass2() 
    myWindow.show()
    app.exec_()