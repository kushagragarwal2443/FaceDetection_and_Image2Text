import zipfile
from zipfile import ZipFile
import PIL
from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

def getisword(image):
    wordinimage=pytesseract.image_to_string(image)
    nonewline=wordinimage.split("\n")
    wordfinal=" ".join(nonewline)
    wordfinal.replace("\n"," ").replace(","," ").replace("."," ")
    getwords=wordfinal.split(" ")
    for word in getwords:
        if word=="Mark":
            return True
    return False

def getlistofimages(image):
    original=image.convert("RGB")
    cversion=image.convert("L")
    cversion.save("imageisthis.png")
    cvimage=cv.imread("imageisthis.png")
    faces = face_cascade.detectMultiScale(cvimage)
    myimages=[]

    for x,y,w,h in faces:
        imaging=original.crop((x,y,x+w,y+h))
        myimages.append(imaging)
    return myimages

def getcontactsheet(listofimages):
    contact_sheet=PIL.Image.new(listofimages[0].mode, (300*5,300*3))
    first_image=listofimages[0]
    x=0
    y=0


    for img in listofimages:
        
        img = img.resize((300,300), Image.ANTIALIAS)
        contact_sheet.paste(img, (x, y) )
    
        if x+300 == contact_sheet.width:
            x=0
            y=y+300
        else:
            x=x+300


    contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
    return(contact_sheet)    

# the rest is up to you
counter=-1
with ZipFile("readonly/images.zip","r") as myfile:
    listofnewspapers=myfile.infolist()

    for newspaper in listofnewspapers:
        with myfile.open(newspaper) as mynewspaper:
            counter=counter+1
            image=Image.open(mynewspaper)
            isword=getisword(image)
            if isword==True:
                print("Results found in file a-{}.png".format(counter))
                listofimages=getlistofimages(image)
                if(len(listofimages)>0):
                    contact_sheet=getcontactsheet(listofimages)
                    display(contact_sheet)
                else:
                    print("But there were no faces in that file!")
            else:
                print("The word not found in the file a-{}.png".format(counter))
