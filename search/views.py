from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json,re,os,pickle
from os import listdir


# Create your views here.
paragraph_filename="paragraph_file.pickle"
invertedIndex_filename="invertedIndex_file.pickle"



def home(request):
    return render(request,"formpage.html",{})

def index(request):
    data=(request.GET.get('input_data'))
    # print(data)
    
    if os.path.exists(paragraph_filename):
    # "with" statements are very handy for opening files. 
        with open(paragraph_filename,'rb') as rfp: 
            paragraphs = pickle.load(rfp)
    else:
        paragraphs=[]
    print(paragraphs)    
    data=data.rstrip()
    paragraph=data.split('\r\n\r\n')
    paragraphs.extend(paragraph)


    if os.path.exists(invertedIndex_filename):
        with open(invertedIndex_filename, 'rb') as handle:
            invertedIndexes = pickle.load(handle)
    else:
        invertedIndexes={}
    print(paragraphs)                   
    for para in paragraph:
        # print('***')
        # print(para)
        words=para.split(' ')
        # print(words)
        for word in words:
            word=word.lower()
            if (word not in invertedIndexes):
                invertedIndexes[word]=[(paragraphs.index(para))]
            else:
                if(paragraph.index(para) not in invertedIndexes[word]):
                    invertedIndexes[word].append(paragraphs.index(para))
    print(invertedIndexes)
    print(os.getcwd())
    with open(paragraph_filename,'wb') as rfp:
        pickle.dump(paragraphs, rfp)
    with open(invertedIndex_filename, 'wb') as handle:
            pickle.dump(invertedIndexes, handle, protocol=pickle.HIGHEST_PROTOCOL)    
    return render(request,"formpage.html",{})

def search(request):
    data=(request.GET.get('input_data'))
    paragaraphs_list=[]
    if os.path.exists(invertedIndex_filename):
        with open(invertedIndex_filename, 'rb') as handle:
            invertedIndexes = pickle.load(handle)
            if data in invertedIndexes:
                if os.path.exists(paragraph_filename):
        # "with" statements are very handy for opening files. 
                    with open(paragraph_filename,'rb') as rfp: 
                        paragraphs = pickle.load(rfp)
                    for ind in invertedIndexes[data]:    
                        paragaraphs_list.append(paragraphs[ind])    
    return render(request,"searchpage.html",{'paragraphs_list':paragaraphs_list})

def clear(request):
    if os.path.exists(paragraph_filename):
        os.remove(paragraph_filename)
    if os.path.exists(invertedIndex_filename):    
        os.remove(invertedIndex_filename)
    # os.chdir(r"D:\TapChief")
    # test=os.listdir(r"tapSearch")
    # print(test)
    # for item in test:
    #     # print(item)
    #     if item.endswith(".pickle"):
    #         print(os.path.join(r'D:\TapChief\tapSearch',item))
    #         os.remove(os.path.join(r'D:\TapChief\tapSearch',item))
    return render(request,"formpage.html",{})    
class TapSearch(APIView):
    def get(self, request, format=None):
        print('*************')
        print(request.GET.get('comments'))
        
