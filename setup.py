
# coding: utf-8

# In[ ]:


# setup.py
from distutils.core import setup
import py2exe
import sys, os
from os import environ
import openalpr
from openalpr import Alpr
datadir = os.path.join('share','data')
datafiles1 = [(d, [os.path.join(d,f) for f in files])
    for d, folders, files in os.walk(datadir)]
datafiles2=[('Images_ressources',['C:\Users\user\Desktop\pfe\OpenCV_3_License_Plate_Recognition_Python\logo_avensys.png'])]
datafiles=datafiles1+datafiles2

sys.setrecursionlimit(5000)

if len(sys.argv)==1:
    sys.argv.append("py2exe")
setup(
    #data_files=[('.',['C:\\Users/user/Anaconda2/Lib/site-packages/openalpr/openalprpy.dll']),('.',['C:\\Users/user/Desktop/pfe/OpenCV_3_License_Plate_Recognition_Python/openalpr.dll')]],
	data_files=datafiles,
	windows=['app.py'],
    options = {
        'py2exe': {
            'includes': ['Tkinter','tkFont','PIL','requests','ttk','cv2','petl','os','datetime','imutils','glob','numpy','openalpr'],
			'packages': ['openalpr'],
        }
	
    }
	#data_files=datafiles, 
)

