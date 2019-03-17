#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 19:47:27 2019

@author: kylebradley
"""
from docx import Document
from nltk.corpus import stopwords


def parse_docx(path):
    document = Document(path)

    lst = []
    for line in document.paragraphs:
        lst.append(line.text)
    
    for index in range(len(lst)):
        lst[index] = lst[index].replace('\t', ' ')
     
    bigList = []
    for line in lst:
        for word in line.split(" "):
            if word in set(stopwords.words('english')) or word =='':
                continue
            bigList.append(word.lower())
    return bigList