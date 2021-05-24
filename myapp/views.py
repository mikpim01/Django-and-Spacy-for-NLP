from django.shortcuts import render
from .models import *
from .forms import Messages

# Create your views here.
import spacy
from spacy.matcher import Matcher
from spacy.util import filter_spans

from django.core.files.storage import FileSystemStorage
import time

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
    time.sleep(2)
    # check if the request is POST means it is from the input form
    if request.method=="POST":
        data=Messages(request.POST)
        if 1:
            # reading the xml file input
            xmldoc = minidom.parse(request.FILES['document'])
            # reading all the object tags in the XML
            itemlist = xmldoc.getElementsByTagName('object')
            finallist = []
            # finding all the class names
            for s in itemlist:
                finallist.append(s.getAttribute("label"))
                # print(s.getAttribute("value"))
            print(finallist) #class Names
            
            # finding all the attributes from the XML diagram
            itemlist = xmldoc.getElementsByTagName('mxCell')
            allValues = []
            for s in itemlist:
                allValues.append(s.getAttribute("value"))
                
            # removing the Function from the class names
            itemlist = xmldoc.getElementsByTagName('object')
            functions = []
            for s in itemlist:
                if s.getAttribute("property")=='func' or s.getAttribute("Property")=='func':
                    functions.append(s.getAttribute("label"))
                print(functions) 
            for s in finallist:
                print(s)
                if s in functions:
                    finallist.remove(s)
            for s in finallist:
                print(s)
                if s in functions:
                    finallist.remove(s)
            for s in finallist:
                print(s)
                if s in functions:
                    finallist.remove(s)
                
                    
            print(finallist)
            associations=[]
            attributes = []
            # filtering the associations (example like 1,1) and attributes from all the MxCell tag in the XML diagram
            for el in allValues:
                try:
                    associations.append(int(el))
                except ValueError:
                    if el != '':
                        if '\n' in el:
                            el = el.replace('\n', ',')
                        if '-' in el:
                            el = el.replace('-', '')
                        
                        print(el)
                        attributes.append(el)
            if '*' in allValues:
                associations.append('*')
            print('Associations are:')
            print(associations)
            print(attributes)
            
            # Code for Nouns extraction using Spacy
            nlp = spacy.load('en_core_web_sm')
            A_np = []
            doc = nlp(request.POST.get('sentence'))
            nouns = []
            for np in doc.noun_chunks:
                    nouns.extend([token.text for token in np])
            
        #   Code for Nouns extraction using Spacy
            
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
            
            listofwords = sentence.split()
            model = Customized._meta.get_field('value')
            customized_sentence = sentence
            
            # replacing single words in the input sentence for SBVR sentence
            for word in listofwords:
                try:
                    obj = Customized.objects.get(value=word)
                    field_value = getattr(obj, 'key')
                    customized_sentence = sentence.replace(word,field_value)
                    # print(field_value)
                except:
                    pass
            

            condition=''
            pointer = 0
            value=''
            # replacing phrases (example: more than) in the input sentence for SBVR sentence
            for i,k in zip(listofwords[0::2], listofwords[1::2]):
                
                try:
                    phrase = str(i+' '+k)
                    obj = Customized.objects.get(value=phrase)
                    field_value = getattr(obj, 'key')
                    customized_sentence = customized_sentence.replace(phrase,field_value)
                except:
                    pass
                # print(i+k)
            
            finallist = [x.lower() for x in finallist]
            common1 = list(set(finallist).intersection(spans))
            common2 = list(set(finallist).intersection(nouns))
            common = len(common1)+len(common2)
            print(nouns)
            print(spans)
            print(common)
            print(finallist)
            notmatch=[]
            finallist = [each_string.lower() for each_string in finallist]

            for s in finallist:
                if s in sentence.lower():
                    pass
                else:
                    notmatch.append(s)
                    print('error at:' + s)
            
            sentence_check='hello'
            if len(notmatch)<1 and (len(nouns)>=1 and len(spans)>=1):
                process='on'
                flag='show'
                sentence_check='on'
                print('if wala')
            elif len(nouns)<1 or len(spans)<1:
                process='off'
                flag='dont'
                sentence_check='off'
                print('elif wala')
            else:
                process = 'off'
                flag='dont'
                print('else wala')
            print(sentence_check)

            # Removing Articles from Nouns
            # if 'The' in nouns:
            #     nouns.remove('The')
            # if 'a' in nouns:
            #     nouns.remove('a')
            # if 'an' in nouns:
            #     nouns.remove('an')
            # if 'A' in nouns:
            #     nouns.remove('A')
            # if 'An' in nouns:
            #     nouns.remove('An')

            for el in nouns:
                try:
                    if el.isdigit():
                        nouns.remove(el)
                except:
                    pass
            # replacing the SBVR sentence according to the phrases in the admin panel / database 
            return render(request,'index.html',{'sentence':request.POST.get('sentence') ,'pos':zip(nouns,spans),'nouns':nouns, 'verbs': spans,'value':value,'condition':condition, 'flag':flag,'button':"Convert To SBVR", 'process': process,'sentence_check': sentence_check,'classnames':finallist,'associations':associations,'notmatch':notmatch,'customized_sentence':customized_sentence,'attributes':attributes})
        # 'button':'It is necessary '+str(customized_sentence)
        else:
            data=Messages()
            respond='Your Message has been sent successfully!'
            return render(request,'index.html',{'response':response})
    respond='Send Message'
    context = {
        'response' : response
        }
    return render(request, 'index.html', context)

def sbvr(request):
    response = 'testing'
    # sleep time
    time.sleep(3)
    # takes the sentence input from the GET request
    sentence = request.GET.get('sentence')
    # spilt the sentence words in a list
    listofwords = sentence.split()
    # find the value in the CUstomized model from the database
    model = Customized._meta.get_field('value')
    # initially the SBVR customized sentence is same as the input sentence
    customized_sentence = sentence
    
    # replacing the SBVR sentence according to the keywords in the admin panel / database
    for word in listofwords:
        try:
            obj = Customized.objects.get(value=word)
            field_value = getattr(obj, 'key')
            customized_sentence = sentence.replace(word,field_value)
            # print(field_value)
        except:
            pass

    # replacing the SBVR sentence according to the phrases in the admin panel / database 
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
    print(customized_sentence)
    print(sentence)
    # rendering the output with all the values passed as context
    return render(request,'index.html',{'sentence':sentence ,'button':"Generate OCL", 'customized_sentence':request.GET.get('customized_sentence'),'condition':request.GET.get('condition'),'value':request.GET.get('value'),'classnames': request.GET.get('classnames')})
       
import ast    
def ocl(request):
    # sleep time
    time.sleep(3)
    condition=''
    value=''

    # picks the sentence from the GET request
    listofwords =request.GET.get('sentence')
    listofwords= listofwords.split()
    # finalizing the condition and value of invariant depending on the conditional input in the SBVR sentence
    check='no'
    for word in listofwords:
        try:
            if str(word) == 'greater than':
                condition='>'
                value=k
                check='yes'
                # print(str(i+' '+k))
            elif str(word) == 'atleast':
                condition='>='
                value=word
                check='yes'
                # print(str(i+' '+k))
            elif str(word) == 'less than':
                condition='<'
                value=word
                check='yes'
                # print(str(i+' '+k))
            elif str(word) == 'atmost':
                condition='<='
                value=word
                check='yes'
                # print(str(i+' '+k))
            elif str(word) == 'exactly':
                condition='='
                value=word
                check='yes'
                # print(str(i+' '+k))
            elif str(word) == 'morethan one':
                condition='>'
                value=word
                check='yes'
                # print(str(i+' '+k))

        except:
            pass
            

    for i,k in zip(listofwords[0::2], listofwords[1::2]):
        try:
            if str(i+' '+k) == 'greater than' or str(i+' '+k) == 'more than':
                condition='>'
                value=k
                print(str(i+' '+k))
            elif str(i) == 'atleast':
                condition='>='
                value=i
                print(str(i+' '+k))
            elif str(i) == 'less than':
                condition='<'
                value=k
                print(str(i+' '+k))
            elif str(i) == 'atmost':
                condition='<='
                value=i
                print(str(i+' '+k))
            elif str(i) == 'exactly':
                condition='='
                value=i
                print(str(i+' '+k))
            elif str(i) == 'morethan one':
                condition='>1'
                value=word
                check='yes'
                print(str(i+' '+k))
            
        except:
            pass
    value= listofwords[listofwords.index(value) + 1]
    print('value '+ str(value))
    print('condition '+ str(condition))

    # rendering the output with all the values passed as context
    return render(request,'index.html',{'sentence': request.GET.get('sentence') ,'button':"Try A New Sentence?", 'customized_sentence': request.GET.get('customized_sentence'),'condition':condition,'value':value,'classnames': ast.literal_eval(request.GET.get('classnames'))})
  