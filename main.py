import cv2 #for image processing
import easygui #to open the filebox
import numpy as np #to store image
import imageio #to read image stored at particular path
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

top=tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image !')
top.configure(background='white')
label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))

def upload():
    imagepath =easygui.fileopenbox()
    cartoonify(imagepath)

def cartoonify(imagepath):
    originalimage = cv2.imread(imagepath)
    originalimage = cv2.cvtColor(originalimage, cv2.COLOR_BGR2RGB)

    if originalimage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

    resized1=cv2.resize(originalimage, (960, 540))

    grayscaleimage = cv2.cvtColor(originalimage, cv2.COLOR_BGR2RGB)
    resized2=cv2.resize(grayscaleimage, (960, 540))
    # plt.imshow(resized2, cmap='gray')

    medianblur=cv2.medianBlur(grayscaleimage, 5)
    resized3=cv2.resize(medianblur, (960, 540))

    getedge= cv2.adaptiveThreshold(medianblur, 255,
                                   cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY, 9,9)
    resized4 = cv2.resize(getedge, (960, 540))

    colorimg=cv2.bilateralFilter(originalimage,9,300,300)
    resized5 = cv2.resize(colorimg, (960, 540))

    cartoonimg = cv2.bitwise_and(colorimg, colorimg, mask=getedge)
    resized6 = cv2.resize(cartoonimg, (960, 540))

    images =[resized1, resized2, resized3, resized4, resized5, resized6]
    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    plt.show()

    #The save Button

    def savebtn(resize6, imagepath):
        newname= "Cartoonified Image"
        location1 = os.path.dirname(imagepath)
        extension = os.path.splitext(imagepath)[1]
        location2 = os.path.join(location1, newname+extension)
        cv2.imwrite(location2, cv2.cvtColor(resized6, cv2.COLOR_RGB2BGR))
        I = "Image saved by name"+ newname+"at"+location2
        tk.messagebox.showinfo(title=None, message=I)

    upload=Button(top,text="Cartoonify an Image",command=upload,padx=10,pady=5)
    upload.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
    upload.pack(side=TOP, pady=50)

    save1 = Button(top, text="Save cartoon image", command=lambda: savebtn(imagepath, resized6), padx=30, pady=5)
    save1.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
    save1.pack(side=TOP, pady=50)

    top.mainloop()


