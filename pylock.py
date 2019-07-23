#!/usr/bin/env python3

'''
Pylock v0.0.1

Compile on MacOS with:
pyinstaller -F -w -i images/icon.ico --hidden-import tkinter --hidden-import tkinter.ttk --hidden-import ttkthemes --hidden-import pymsgbox --hidden-import pycrypto --add-data 'images/bg.jpg:images' pylock.py
'''

import os, sys, time, hashlib, platform, getpass
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from ttkthemes import ThemedStyle
from PIL import ImageTk, Image
from Crypto import Random
from Crypto.Cipher import AES
from pymsgbox import *

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(file_name, save, key):
    with open(file_name, 'rb') as f:
        plaintext = f.read()
    enc = encrypt(plaintext, key)
    with open(save + ".zez", 'wb') as f:
        f.write(enc)

def decrypt_file(file_name, save, key):
    with open(file_name, 'rb') as f:
        ciphertext = f.read()
    dec = decrypt(ciphertext, key)
    with open(save[:-4], 'wb') as f:
        f.write(dec)

class MainWindow(Tk):
    #def __init__(self, username, pwd):
    def __init__(self):
        Tk.__init__(self)
        self.title(string = "Pylock v0.1")
        self.resizable(0,0)
        self.ttkStyle = ThemedStyle()
        self.ttkStyle.set_theme("blue")
        self.configure(background = 'white')
        '''
        icon = ImageTk.PhotoImage(Image.open(resource_path('images/icon.png')))
        #icon = PhotoImage(file='icon.png') # <-- Linux and Windows only, the line above is for MacOS
        self.tk.call('wm', 'iconphoto', self._w, icon)
        '''
        self.eval('tk::PlaceWindow %s center' % self.winfo_pathname(self.winfo_id()))
        self.protocol("WM_DELETE_WINDOW", self.on_close_event)

        self.bind("<Escape>", self.exit) # Press ESC to quit app


        self.options = {
            'username' : StringVar(),
            'pwd' : StringVar(),
            'file' : StringVar(),
            'save_location' : StringVar(),
            'decryptpassword' : StringVar(),
            'encryptpassword' : StringVar(),
        }

        photo = Image.open(resource_path('images/bg.jpg'))
        resized = photo.resize((280,280), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized)

        label = Label(self, image=photo, background = 'white')
        label.image = photo # keep a reference!
        label.grid(row = 0, column = 0, columnspan = 2, rowspan = 2)

        decrypt_clk = Button(self, text = 'Decrypt', command = self.file_open_decrypt, width = 18).grid(row = 4, column = 0, columnspan = 1, sticky = 'w')
        encrypt_clk = Button(self, text = 'Encrypt', command = self.file_open_encrypt, width = 18).grid(row = 4, column = 1, columnspan = 1, sticky = 'w')

    def enc_file(self):
        self.options['encryptpassword'] = password(text='Set a password for your file', title='Encrypt', mask='*')
        if self.options['encryptpassword'] == '':
            opt = messagebox.showwarning('Error', 'Please enter a password to encrpyt the file')
            return self.enc_file()
        elif self.options['encryptpassword'] == None:
            pass
        else:
            if platform.system() == 'Darwin':
                self.options['save_location'] = '/Users/' + getpass.getuser() + '/Desktop/' + self.options['file'].split('/')[-1]
            else:
                self.options['save_location'] = self.options['file']

            self.encrypt_now()

    def dec_file(self):
        self.options['decryptpassword'] = password(text='Set a password for your file', title='Decrypt', mask='*')
        if self.options['decryptpassword'] == '':
            opt = messagebox.showwarning('Error', 'Please the password to decrypt your file')
            return dec_file()
        elif self.options['decryptpassword'] == None:
            pass
        else:
            if platform.system() == 'Darwin':
                self.options['save_location'] = '/Users/' + getpass.getuser() + '/Desktop/' + self.options['file'].split('/')[-1]
            else:
                self.options['save_location'] = self.options['file']
            self.decrypt_now()

    def decrypt_now(self):
        key = hashlib.sha256(self.options['decryptpassword'].encode('utf-8')).digest() # Set key
        '''
        print(self.options['decryptpassword'])
        print(key)
        '''
        decrypt_file(self.options['file'], self.options['save_location'], key)


    def encrypt_now(self):
        key = hashlib.sha256(self.options['encryptpassword'].encode('utf-8')).digest() # Set key
        '''
        print(self.options['encryptpassword'])
        print(key)
        '''
        encrypt_file(self.options['file'], self.options['save_location'], key)


    def file_open_encrypt(self):
        self.options['file'] =  askopenfilename()
        if self.options['file'] == '':
            return
        self.title(string = 'Encrypt file: %s' % self.options['file'])
        self.enc_file()

    def file_open_decrypt(self):
        self.options['file'] = askopenfilename()
        if self.options['file'] == '':
            return
        self.title(string = 'Decrypt file: %s' % self.options['file'])
        self.dec_file()

    def exit(self, event):
        self.on_close_event()

    def on_close_event(self):
        result = messagebox.askyesno("Are you sure?","Are you sure you want to exit?")
        if result == False:
            return
        else:
            pass

        sys.exit(0)

main = MainWindow()
main.mainloop()
