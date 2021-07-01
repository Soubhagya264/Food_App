from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import Contact,Order
from .models import  Myadm
from .forms import CreateUserForm , Itemform
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from tensorflow.python.framework import ops
import nltk
from nltk.stem.lancaster import LancasterStemmer
from django.http import JsonResponse
import tensorflow as tf
import numpy as np
import tflearn
import random
import json
import pickle

def chatbot(request):
  if request.method=='POST':
      sen=request.POST.get('chat_bot')      
      data=pickle.load(open("C:\\Users\\HP\\my_rest_web\\Restaurant_project\\Food_app\\rest_proj_app\\training_data","rb"))
      words=data['words']
      classes=data['classes']
      train_x=data['train_x']
      train_y=data['train_y']
      ops.reset_default_graph()
      net=tflearn.input_data(shape=[None,len(train_x[0])])
      net=tflearn.fully_connected(net,10)
      net=tflearn.fully_connected(net,10)
      net=tflearn.fully_connected(net,len(train_y[0]),activation='softmax')
      net=tflearn.regression(net)
      model=tflearn.DNN(net,tensorboard_dir="tflearn_logs")
      model.load('C:\\Users\\HP\\my_rest_web\\Restaurant_project\\Food_app\\rest_proj_app\\model.tflearn')
      stemmer=LancasterStemmer()
      with open('C:\\Users\\HP\\my_rest_web\\Restaurant_project\\Food_app\\rest_proj_app\\intents.json') as json_data:
        intents=json.loads(json_data.read())
      def clean_up_sentence(sentence):
            sentence_words=nltk.word_tokenize(sentence)
            sentence_words=[stemmer.stem(word.lower()) for word in sentence_words]
            return sentence_words
      def bow(sentence,words,show_details=False):
            sentence_words=clean_up_sentence(sentence)
            bag=[0]*len(words)
            for s in sentence_words:
                for i,w in enumerate(words):
                    if w==s:
                        bag[i]=1
                        if show_details:
                            print("found in bag:%s"%w)
            return (np.array(bag))
      context={}
      ERROR_THRESHOLD=0.30
      def classify(sentence):
          results=model.predict([bow(sentence,words)])[0]
          
          results=[[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
          results.sort(key=lambda x:x[1] ,reverse=True)

          return_list=[]
          for r in results:
              return_list.append((classes[r[0]],r[1]))
          return return_list    
      def response(sentence,userID='123',show_detail=False):
          results=classify(sentence)
          if results:
              while results:
                  for i in intents['intents']:
                      if i['tag']==results[0][0]:
                          if 'context_set' in i:
                              if show_detail:
                                  print('context:' ,i['context_set'])
                              context[userID]=i['context_set']
                          if not 'context_filter' in i or (userID in context and 'context-filter' in i and i['context_filter']==context[userID]):  
                              if show_detail: 
                                  print ('tag:', i['tag'])
                              return (random.choice(i['responses']))
              results.pop(0) 
      res=response(sen)
      print(res)
      return JsonResponse({'result':res},status=200)
                        
# hello("what are your hours of operation?")  


    
def main_home(request):

  if request.method=='POST':
    if request.POST.get('name'):
      contact=Contact()
      name=request.POST.get('name')
      email=request.POST.get('email')
      ph_no=request.POST.get('ph_no')
      msg=request.POST.get('msg')
      contact.name=name
      contact.email=email
      contact.ph_no=ph_no
      contact.msg=msg
      contact.save()
      c=Contact.objects.all()
      print(c)
      return HttpResponse("<div style='border:2px solid black';display: block;margin-left: auto;margin-right: auto;width: 10%;><h1 style='text-align:center;'>Thanks for Contacting</h1></div>")

  S_form=CreateUserForm()
  if request.method=='POST':
    if request.POST.get('SignUp'):
        S_form=CreateUserForm(request.POST)
        print(S_form.data['username'])

        if S_form.is_valid():
          S_form.save()
          print("SAVE")
        else:
          return HttpResponse("please again fill the valid data to signup form")
        return render(request,'index.html')
  if request.method=='POST':
    if request.POST.get('Login_'):
      username=request.POST.get('uname')
      password=request.POST.get('password')
      print(username,password)

      user=authenticate(request,username=username,password=password)
      if user is not None:
        login(request,user)
        return render(request,'index.html')
      else:
        return HttpResponse("<h1> Please put the valid username or password</h1>")

  form_dic={'S_form':S_form}
  res=render(request,'index.html',context=form_dic)
  return res




def menu(request):
  item_data=Myadm.objects.all()
  item=[]
  d={}
  i_name=None
  itm=None
  if request.method=="POST" and request.POST.getlist('iname') :
    i_name=request.POST.getlist('iname') 
    print(i_name)
    try:
          for i in i_name:
            item.append(i.split(','))
            for i in item:
              for x in i:
                  k , v =x.split(':')
                  d[k]=int(v)
          print(d)        
    except Exception as e:
      print(e)              
    
    return render(request,'Admin-item.html',{'d':d})
  
  if request.method=="POST" and request.POST.get('items'):
    item= request.POST.get('items')
    price=request.POST.get('price')
    name= request.POST.get('name')
    email=request.POST.get('email')
    address=request.POST.get('address')
    city=request.POST.get('city')
    ph_no=request.POST.get('phone')
    
    print(item,price,name,email)
    # return render(request,'menu.html',{'item_data':item_data})
    
    order=Order()
    order.item=item
    order.price=price
    order.name=name
    order.email=email
    order.address=address
    order.city=city
    order.ph_no=ph_no
    order.save()
    print(Order.objects.all())
  
  
  return render(request,'menu.html',{'item_data':item_data})
