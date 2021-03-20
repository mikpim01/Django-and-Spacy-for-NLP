from django.shortcuts import render
from .models import *
from .forms import Messages

# Create your views here.
import spacy
from spacy.matcher import Matcher
from spacy.util import filter_spans
            
def index(request):
    form = Messages()
    return render(request, 'index.html', {'form': form, 'button': 'show'})


def submit(request):
    response = 'testing'
            
    if request.method=="POST":
        data=Messages(request.POST)
        if data.is_valid():
            # data.save()
        #    for noun extraction
            nlp = spacy.load('en_core_web_sm')
            A_np = []
            doc = nlp(request.POST.get('sentence'))
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
            
            listofwords = sentence.split()
            print(listofwords)
            model = Customized._meta.get_field('value')
            customized_sentence = ''
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
                    print(phrase)
                    obj = Customized.objects.get(value=phrase)
                    field_value = getattr(obj, 'key')
                    print(field_value)
                    customized_sentence = customized_sentence.replace(phrase,field_value)
                    print(customized_sentence)
                except:
                    pass
                # print(i+k)
            # print(customized_sentence)
            return render(request,'index.html',{'sentence':request.POST.get('sentence') ,'pos':zip(nouns,spans), 'verbs': spans, 'flag':'show','button':str(customized_sentence)})
        else:
            data=Messages()
            respond='Your Message has been sent successfully!'
            return render(request,'index.html',{'response':response})
    respond='Send Message'
    context = {
        'response' : response
        }
    return render(request, 'index.html', context)

