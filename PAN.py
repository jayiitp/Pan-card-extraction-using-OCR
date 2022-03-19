#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Install ftfy


# In[2]:


pip install ftfy


# In[3]:


#Import


# In[4]:


from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
import io
import json
import ftfy


# In[5]:


#PreProcessing Image


# In[7]:


img = Image.open('pan_card.jpg')
img = img.convert('RGBA')
#img.show()
pix = img.load()


# In[8]:


for y in range(img.size[1]):
    for x in range(img.size[0]):
        if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
            pix[x, y] = (0, 0, 0, 255)
        else:
            pix[x, y] = (255, 255, 255, 255)

img.save('temp.png')
#img.show()


# In[9]:


image = cv2.imread('temp.png')
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
gray = cv2.medianBlur(image, 3)


# In[10]:


#Extract String through Image


# In[11]:


pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
text = pytesseract.image_to_string(gray)
text=re.sub(r'[^\x00-\x7F*]+',' ', text)


# In[13]:


#print(text)


# In[14]:


text_output = open('outputbase.txt', 'w', encoding='utf-8')
text_output.write(text)
text_output.close()


# In[16]:


file = open('outputbase.txt', 'r', encoding='utf-8')
text = file.read()
#print(text)


# In[18]:


text = ftfy.fix_text(text)
text = ftfy.fix_encoding(text)
#'''for god_damn in text:
#    if nonsense(god_damn):
#        text.remove(god_damn)
#    else:
#        print(text)'''
#print(text)


# In[19]:


name = None
fname = None
dob = None
pan = None
nameline = []
dobline = []
panline = []
text0 = []
text1 = []
text2 = []


# In[21]:


lines = text.split('\n')
for lin in lines:
    s = lin.strip()
    s = lin.replace('\n','')
    s = s.rstrip()
    s = s.lstrip()
    text1.append(s)

text1 = list(filter(None, text1))
#print(text1)


# In[23]:


lineno = 0
for wordline in text1:
    xx = wordline.split('\n')
    if ([w for w in xx if re.search('(INCOMETAXDEPARWENT @|mcommx|INCOME|er ae|TAX|GOW|ey|GOVT|GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA)$', w)]):
        text1 = list(text1)
        lineno = text1.index(wordline)
        break

# text1 = list(text1)
text0 = text1[lineno+1:]

stopwords = ["'Sires 4 faapt","Siraeey faant","INCOME TAX DEPARTMENT","er ae","aay ad","ae","INCOMETAX DEPARTMENT  @@ = GOVT. OF INDIA -","ee","Preeannend Account Mumber","Signature","Dwwrkamaler","MeNIKA M -SHIN DE","MONIKA M4 -oHINDE","Stgnature","Pasmanent Account Number","Permanent Account Number .","GOVT. OF INDIA","Permanent Account Number"]
text0 = [word for word in text0 if word not in stopwords]

#print(text0)  # Contains all the relevant extracted text in form of a list - uncomment to check


# In[24]:


name = text0[0]
fname = text0[1]
dob = text0[2]
pan = text0[3]


# In[25]:


data = {}
data['Name'] = name
data['Father Name'] = fname
data['Date of Birth'] = dob
data['PAN'] = pan

print(data)


# In[ ]:





# In[ ]:




