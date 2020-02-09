#!/usr/bin/env python
# coding: utf-8

# In[3]:


#functions_to_use
#variables:
# variables



# build the HTTP digest auth

#here we will define all our functions to use in the application
###############################################################
#imports
import petl as etl #to manage csv and xlsx file
import requests # to get images from the camera
from requests.auth import HTTPDigestAuth
try:
 
    import tkinter as tk #python 3
    from tkinter import ttk as ttk
except:
    import Tkinter as tk     # python 2
    import ttk as ttk
import cv2
#USER = "root"
#PASS = "root"
#HOSTNAME = "http://192.168.1.14:1025"

#URL =  HOSTNAME + "/axis-cgi/jpg/image.cgi"
##################################################################
def download_image(url,USER,PASS, filename=None):
        DIGEST = HTTPDigestAuth(username=USER, password=PASS)
        """
        Download a file - optionally with a filename
        :param url: URL to be requested
        :param filename: optional filename
        :return: output filename
        """
        # take filename if provided
        if filename:
            local_filename = filename
        else:
            local_filename = url.split('/')[-1]

        # NOTE the stream=True parameter
        r = requests.get(url, auth=DIGEST, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
        return local_filename
#the combine function is used to allow a widget to execute diffrent actions at one click  
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

def download_file(win,value):
    from tkinter import filedialog
    import requests
    #here we are going to nstatantiate the save as window 
    win.filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("Excel files","*.xls"),("all files","*.*")))
    #reading the entred date and storing it
    selected_date=value
    dir=win.filename+".csv"
    
    #data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT&apikey=demo&datatype=csv')
                #with open(dir, 'w') as f:
                 #   writer = csv.writer(f)
                  #  reader = csv.reader(data.text.splitlines())

                   # for row in reader:
                    #    writer.writerow(row)
    #Load the table from the result file wghich the timestamp colomun corresponded to the given date
    table1 = etl.fromcsv(r'C:\avenguard\files\results.csv')
    table2 = etl.rowlenselect(table1, 12)
    # Alter the colums
    table2 = etl.cut(table2, 'plate','timestamp')
                
    #table2 = etl.tail(table2, 15)
    table2 = etl.select(table2, lambda rec: rec.timestamp.split("_")[0] == selected_date )    
    # Save to new file in format xmls (excel file)
    #etl.tocsv(table2, dir)
    etl.toxlsx(table2, win.filename+'.xlsx')
    
def insert_type(string):
     
    s=string.replace('G','6')
    s=s.replace('I','1')
    s=s.replace('S','5')
    s=s.replace('O','0')
    s=s.replace('Q','0')
    s=s.replace('D','0')
    s=s.replace('B','8')
    s=s.replace('E','3')
    if len(s)==8:  
        s=s[:2] + '-' + s[2:]
    elif len(s)==7:
        s=s[:3] + ' TU ' + s[3:]
    elif len(string)==6:
        s=s[:2] + ' TU ' + s[2:]
    return s

def compare_plates(im1,im2):
            # Initiate SIFT detector
            sift = cv2.xfeatures2d.SIFT_create()
            img1=cv2.imread(im1,0)
            img2=cv2.imread(im2,0)
            # find the keypoints and descriptors with SIFT
            try:
                kp1, des1 = sift.detectAndCompute(img1,None)
            except:
                print("Image not found")
            try:
                kp2, des2 = sift.detectAndCompute(img2,None)
            except:
                kp2, des2 = sift.detectAndCompute(img1,None)
            # BFMatcher with default params
            bf = cv2.BFMatcher()
            try:
                matches = bf.knnMatch(des1,des2, k=2)
            except:
                matches = bf.knnMatch(des1,des2, k=2) 

            #print(len(matches))
            # Apply ratio test
            good = []
            for m,n in matches:
                if m.distance < 0.75*n.distance:
                    good.append([m])
            #print (len(good)) 
            return (len(good))>100
def get_camera_data():
        fileHandle = open ( r'C:\avenguard\files\IPAddress.txt',"r" )
        lineList = fileHandle.readlines()
        fileHandle.close()
        s=lineList[-1]
        url=''
        dir="C:/avenguard/temporary_images"
        i=0 
        for char in s:
            if (i<len(s)-1):
                url=url+char
                i=i+1
        USER=url.split(':')[0]
        PASS=url.split(':')[1].split('@')[0]
        HOSTNAME=url.split('@')[1]
        return USER, PASS, HOSTNAME
def transform_data(df):
    df=df[['plate', 'timestamp', 'region']]
    df['plate'] = df['plate'].apply(lambda x: insert_type(x))
    return (df)
