# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 11:04:48 2022

@author: Fatima Khalid
"""

import os
from PIL import Image
from pdf2image import convert_from_path
import numpy
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 850, height = 500, bg = 'white', relief = 'raised')
canvas1.pack()

label1 = tk.Label(root, text='PDF Color Dectection Tool ', bg = 'white' , fg = '#0583D2',)
label1.config(font=('poppins', 22))
canvas1.create_window(450, 60, window=label1)

# files = os.listdir('C:/Users/Fatima Khalid/.spyder-py3/Files') ## Dir Path of pdf Files

def getImage():
     # for file in files: #iterate through the list of files in the directoy
       
        global import_file_path
        import_file_path = filedialog.askopenfilename()
        global images 
        images = convert_from_path(import_file_path) #concat the absoulte path with the file name     
        image = images.pop()
        #Get the image
        # print(file) 
        checkImage(image)
        # print(import_file_path)         



browseButton = tk.Button(text="     Select File     ", command=getImage, bg='#293B5F', fg='white', font=('poppins', 12 ))
canvas1.create_window(450, 150, window=browseButton)

def checkImage(image):
    #Cropping Image
    width, height = image.size
    left = width / 6
    top = height / 6
    right = 5 * width / 6
    bottom = 5 * height / 6
    image = image.crop((left, top, right, bottom))
   # image.show() can be used to show each image after cropping

    #Getting Image RGB Information
    width, height = image.size
    pixel_values = list(image.getdata())
    if image.mode == "RGB": # For RGB Images
        channels = 3
    elif image.mode == "L": # For Gray Scale Images
        channels = 16
    pixel_values = numpy.array(pixel_values).reshape((width, height, channels)) # 2D Array of Image Pixels

    greyscale = True 
    rich_Black = True
    for pic in pixel_values:
        for pi in pic:
            r,g,b = pi
            avg = (r+g+b)/3 #Average of RGB Values
            if not (avg == 255): 
                
                #if not checkgray(pi):
                    
                if not ( avg <= 25): ## For rich Black Check
                    rich_Black = False
                if not ( (abs(avg-r)<9) and (abs(avg-g)<9) and (abs(avg-b)<9) ): ##to idendify if the image is greyscale or not 
                    greyscale = False
                    
      #print(pi)
      #for pic in pixel_values:
      # print(pic[0])
    if rich_Black:
        tk.messagebox.showinfo("Result","Rich Black_Expected: Ask to customers full color or monochrome because of Rich black")
        # print("Rich Black_Expected: Ask to customers full color or monochrome because of Rich black")
    elif greyscale:
        tk.messagebox.showinfo("Result","Expected Monochrome")

        # print("Expected Monochrome")
    else:
        tk.messagebox.showinfo("Result","Expected Full Color")
       
        # print("Expected Full Color")   




def exitApplication():
    MsgBox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'warning')
    if MsgBox == 'yes':
       root.destroy()
     
exitButton = tk.Button (root, text='          Exit          ',command=exitApplication, bg='#293B5F', fg='white', font=('poppins', 12))
canvas1.create_window(450, 230, window=exitButton)

root.mainloop()
    