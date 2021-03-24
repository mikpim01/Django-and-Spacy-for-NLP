from django.shortcuts import render
from .models import *
from .forms import Messages

# Create your views here.
import spacy
from spacy.matcher import Matcher
from spacy.util import filter_spans

from django.core.files.storage import FileSystemStorage


def index(request):
    form = Messages()
    return render(request, 'index.html', {'form': form, 'button': 'show'})


# def submit(request):
#     response = 'testing'
            
#     if request.method=="POST" and request.FILES['myfile']:
#         data=Messages(request.POST,request.FILES)
        
#         if data.is_valid():
#             # data.save()
#         #    for noun extraction
#             nlp = spacy.load('en_core_web_sm')
#             A_np = []
#             doc = nlp(request.POST.get('sentence'))
#             nouns = []
#             for np in doc.noun_chunks:
#                     nouns.extend([token.text for token in np])
#             # A_np.append(sent_nps)

#         # for verb extraction
            
#             nlp2 = spacy.load('en_core_web_sm') 

#             sentence = request.POST.get('sentence')
#             pattern = [{'POS': 'VERB', 'OP': '?'},
#                        {'POS': 'ADV', 'OP': '*'},
#                        {'POS': 'AUX', 'OP': '*'},
#                        {'POS': 'VERB', 'OP': '+'}
#                        ]

#             # instantiate a Matcher instance
#             matcher = Matcher(nlp2.vocab)
#             matcher.add("Verb phrase", None, pattern)

#             doc = nlp2(sentence) 
#             # call the matcher to find matches 
#             matches = matcher(doc)
#             spans = [doc[start:end] for _, start, end in matches]
#             # print(data['sentence'])
#             print(request.POST['sentence'])
#             listofwords = sentence.split()
#             print(listofwords)
#             model = Customized._meta.get_field('value')
#             customized_sentence = ''
#             for word in listofwords:
#                 try:
#                     obj = Customized.objects.get(value=word)
#                     field_value = getattr(obj, 'key')
#                     customized_sentence = sentence.replace(word,field_value)
#                     # print(field_value)
#                 except:
#                     pass
            
#             for i,k in zip(listofwords[0::2], listofwords[1::2]):
                
#                 try:
#                     phrase = str(i+' '+k)
#                     print(phrase)
#                     obj = Customized.objects.get(value=phrase)
#                     field_value = getattr(obj, 'key')
#                     print(field_value)
#                     customized_sentence = customized_sentence.replace(phrase,field_value)
#                     print(customized_sentence)
#                 except:
#                     pass
#                 # print(i+k)
#             print(customized_sentence)
#             return render(request,'index.html',{'sentence':request.POST.get('sentence') ,'pos':zip(nouns,spans), 'verbs': spans, 'flag':'show','button':'It is necessary '+str(customized_sentence)})
#         else:
#             data=Messages()
#             respond='Your Message has been sent successfully!'
#             return render(request,'index.html',{'response':response})
#     respond='Send Message'
#     context = {
#         'response' : response
#         }
#     return render(request, 'index.html', context)

import json 
import xmltodict 
from xml.dom import minidom


def submit(request):
    response = 'testing'
            
    if request.method=="POST":
        data=Messages(request.POST)
        
        if 1:
            # data.save()
        #    for noun extraction
            # myfile = request.FILES['document']
            print(request.FILES['document'])
            xmldoc = minidom.parse(request.FILES['document'])
            print(xmldoc)
            itemlist = xmldoc.getElementsByTagName('mxCell')
            finallist = []
            for s in itemlist:
                finallist.append(s.getAttribute("value"))
                print(s.getAttribute("value"))
            print(finallist)
            
            nlp = spacy.load('en_core_web_sm')
            A_np = []
            doc = nlp(request.POST.get('sentence'))
            # print(request.POST.get('document'))
            nouns = []
            for np in doc.noun_chunks:
                    nouns.extend([token.text for token in np])
            # A_np.append(sent_nps)

        # for verb extraction
            
            nlp2 = spacy.load('en_core_web_sm') 

            sentence = request.POST.get('sentence')
            pattern = [{'POS': 'VERB', 'OP': '?'},
                       {'POS': 'ADV', 'OP': '*'},
                       {'POS': 'AUX', 'OP': '*'},
                       {'POS': 'VERB', 'OP': '+'}
                       ]

            # instantiate a Matcher instance
            matcher = Matcher(nlp2.vocab)
            matcher.add("Verb phrase", None, pattern)

            doc = nlp2(sentence) 
            # call the matcher to find matches 
            matches = matcher(doc)
            spans = [doc[start:end] for _, start, end in matches]
            # print(data['sentence'])
            # print(request.POST['sentence'])
            listofwords = sentence.split()
            # print(listofwords)
            model = Customized._meta.get_field('value')
            customized_sentence = sentence
            for word in listofwords:
                try:
                    obj = Customized.objects.get(value=word)
                    field_value = getattr(obj, 'key')
                    customized_sentence = sentence.replace(word,field_value)
                    # print(field_value)
                except:
                    pass
            
            for i,k in zip(listofwords[0::2], listofwords[1::2]):
                
                try:
                    phrase = str(i+' '+k)
                    # print(phrase)
                    obj = Customized.objects.get(value=phrase)
                    field_value = getattr(obj, 'key')
                    # print(field_value)
                    customized_sentence = customized_sentence.replace(phrase,field_value)
                    # print(customized_sentence)
                except:
                    pass
                # print(i+k)
            # print(customized_sentence)
            finallist = [x.lower() for x in finallist]
            common1 = list(set(finallist).intersection(spans))
            common2 = list(set(finallist).intersection(nouns))
            common = len(common1)+len(common2)
            print(common2)
            if common>=2:
                process='on'
                flag='show'
            else:
                process = 'off'
                flag='dont'
            return render(request,'index.html',{'sentence':request.POST.get('sentence') ,'pos':zip(nouns,spans), 'verbs': spans, 'flag':flag,'button':'It is necessary '+str(customized_sentence), 'process': process})
        else:
            data=Messages()
            respond='Your Message has been sent successfully!'
            return render(request,'index.html',{'response':response})
    respond='Send Message'
    context = {
        'response' : response
        }
    return render(request, 'index.html', context)

