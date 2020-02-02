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
#datafiles1 = [(d, [os.path.join(d,f) for f in files])
#    for d, folders, files in os.walk(datadir)]
datafiles=[('.',['logo_avensys.png','To_ico.ico'])]
#datafiles=datafiles1+datafiles2

sys.setrecursionlimit(5000)

if len(sys.argv)==1:
    sys.argv.append("py2exe")
setup(
    
    data_files=datafiles,
    windows=['av.py'],
    options = {
        'py2exe': {
            "dll_excludes": ["MSVFW32.dll",
                 "AVIFIL32.dll",
                 "AVICAP32.dll",
                 "ADVAPI32.dll",
                 "CRYPT32.dll",
                 "WLDAP32.dll"],
            'includes': ['Tkinter','tkFont','PIL','requests','ttk','cv2','petl','os','datetime','imutils','glob','numpy','openalpr'],
            'packages': ['openalpr']
        }
    
    }
     
)

