import subprocess
import hashlib
import math
import decrypt_pack
import encrypt_pack
import csv
import helper
from helper import *
import zipfile
import io
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
import kivy
from kivy.app import App
from kivy.uix.button import Button
from plyer import filechooser


output_path = "game_files"
lists_paths = "decrypted_lists"


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

class MyApp(App):
    def build(self):
        button = Button(text='Open File Browser')
        button.bind(on_release=self.open_file_browser)
        return button
    
    def open_file_browser(self, *args):
        def on_selection(selection):
            # Handle the selected file(s) here
            if selection:
                selected_path = selection[0]
                print("Selected file:", selected_path)
                return selected_path

        # Use AndroidFileChooser to open the default file browser
        filters = [("PACK Files", "*.pack")]
        path = filechooser.open_file(on_selection, filters=filters)
        print(path)
        


if __name__ == "__main__":
    MyApp().run()

