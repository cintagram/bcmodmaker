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
from pyobjus import autoclass, objc_str


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

# Define the file selection function
def select_file(instance):
    # Use the NSOpenPanel to display the file selection dialog
    NSOpenPanel = autoclass('NSOpenPanel')
    panel = NSOpenPanel.openPanel()

    # Configure the panel for file selection
    panel.setCanChooseFiles_(True)
    panel.setCanChooseDirectories_(False)
    panel.setAllowsMultipleSelection_(False)

    # Set the panel's title and message
    panel.setTitle_(objc_str('Select Byte File'))
    panel.setMessage_(objc_str('Choose a byte file'))

    # Set the panel's allowed file types
    allowed_types = ['public.data']  # Add any desired UTIs or file types
    panel.setAllowedFileTypes_(allowed_types)

    # Display the panel and handle the result
    if panel.runModal() == 1:
        # Get the selected file URL
        url = panel.URLs().firstObject()

        # Convert the URL to a file path
        file_path = str(url.path())

        # Process the selected file as a byte file
        with open(file_path, 'rb') as file:
            byte_data = file.read()

        # Perform further actions with the byte data
        print(byte_data)

# Create a simple Kivy app to demonstrate the file selection
class MyApp(App):
    def build(self):
        button = Button(text='Select Byte File')
        button.bind(on_release=select_file)
        




