from django.shortcuts import render,redirect
from dashboard.models import Note,Homework,Todo
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from PyDictionary import PyDictionary

def home(request):
    return render(request,"home.html")

@login_required
def notes(request):
    if request.method=='POST':
        title=request.POST['title']
        description=request.POST['description']
        ins=Note(user=request.user,title=title,description=description)
        ins.save()
        messages.success(request,f"Note Creared:{request.user}")
    notes=Note.objects.filter(user=request.user)
    context={"notes":notes}        
    return render(request,'notes.html',context)

@login_required
def notesdelete(request,nid):
    note=Note.objects.get(id=nid)
    note.delete()
    return redirect("/notes")

@login_required
def notesdetail(request,name):
    note=Note.objects.filter(title=name).first()
    context={"note":note}
    return render(request,'notesdetail.html',context)

@login_required
def homework(request):    
    if request.method=='POST':
        try:
            finished=request.POST['homeworkcheck']
            if finished=='1':
                finished=True
            else:
                finished=False   
        except:
            finished=False      
        subject=request.POST['subject']
        title=request.POST['title']
        description=request.POST['description']
        due=request.POST['due']
        ins=Homework(user=request.user,subject=subject,title=title,description=description,due=due,isfinished=finished)
        ins.save()
    homework=Homework.objects.filter(user=request.user)
    if len(homework)==0:
        homework_done=True
    else:
        homework_done=False
    context={"homework":homework,"homework_done":homework_done}
    return render(request,'homework.html',context)

@login_required
def updatehomework(request,hid):
    homework=Homework.objects.get(id=hid,user=request.user)
    if homework.isfinished==True:
        homework.isfinished=False
    else:
        homework.isfinished=True
    homework.save()
    return redirect("/homework")   

@login_required
def deletehomework(request,hid):
    Homework.objects.get(id=hid,user=request.user).delete() 
    return redirect("/homework")

def youtube(request):
    if request.method=='POST':
        text=request.POST['search']
        video=VideosSearch(text,limit=10)    
        result_list=[]
        for i in video.result()['result']:  
            result_dict={    
                'input':text,    
                'title':i['title'],      
                'duration':i['duration'],
                'thumbnails':i['thumbnails'][0]['url'],      
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }
            desc=""
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                   desc+=j['text']
            result_dict['description']=desc
            result_list.append(result_dict) 
            context={"results":result_list}
        return render(request,"youtube.html",context)        

    return render(request,'youtube.html')

@login_required
def todo(request):
    if request.method=='POST':
        try:
            finished=request.POST['todocheck']
            if finished=='1':
                finished=True
            else:
                finished=False
        except:
            finished=False  
        title=request.POST['title']
        ins=Todo(user=request.user,title=title,isfinished=finished)
        ins.save()
    todos=Todo.objects.filter(user=request.user)
    if len(todos)==0:
        tododone=True
    else:
        tododone=False
    context={"todos":todos,"tododone":tododone}                                 
    return render(request,'todo.html',context)

@login_required
def updatetodo(request,tid):
    todo=Todo.objects.get(id=tid,user=request.user)
    if todo.isfinished==True:
        todo.isfinished=False
    else:
        todo.isfinished=True
    todo.save()
    return redirect("/todo")      

@login_required
def deletetodo(request,tid):
     todo=Todo.objects.get(id=tid,user=request.user).delete()
     return redirect("/todo")

def books(request):
    if request.method=='POST':
        text=request.POST['search']
        url="https://www.googleapis.com/books/v1/volumes?q="+text      
        r=requests.get(url)    
        answer=r.json()      
        result_list=[]
        for i in range(10):  
            result_dict={   
                
                'title':answer['items'][i]['volumeInfo']['title'],  
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink')   
            }
            result_list.append(result_dict) 
            context={"results":result_list}
        return render(request,"books.html",context)  
    return render(request,"books.html")

def  dictionary(request):
    if request.method=='POST':
        search=request.POST['searchtext']
        dictionary=PyDictionary()
        try:
           definition=dictionary.meaning(search)
           if definition.get('Verb'): 
             definition=definition['Verb']          
           elif definition.get('Noun'):
             definition=definition['Noun']
           elif definition.get('Adjective'):
              definition=definition['Adjective']
           context={'definition':definition,'input':search} 
        except:  
             context={'input':''}           
        return render(request,'dictionary.html',context)               
    return render(request,'dictionary.html')

def wiki(request):                 
    if request.method=='POST':                   
        text=request.POST['text']           
        search=wikipedia.page(text)
        context={
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,'wiki.html',context)  
    return render(request,'wiki.html')       


def register(request):
    if request.method=='POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['password1']
        pass2=request.POST['password2']

        if pass1!=pass2:
            messages.error(request,"Password not match")
            return redirect('/register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request,"user exist")
            return redirect("/register")
        else:
            myuser=User.objects.create_user(username,email,pass1)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.save()
            messages.success(request,"Signup successful")  
            login(request,myuser)
            return redirect("/")   
    return render(request,'register.html')

def fnlogin(request):
    if request.user.is_authenticated:
        messages.success(request,f"The user {request.user} Login")
        return redirect("/") 
    else:
        if request.method=="POST":
            usernamelogin=request.POST['usernamelogin']
            passwordlogin=request.POST['passwordlogin']       
            user=authenticate(username=usernamelogin,password=passwordlogin)
            if user is not None:
               login(request,user)
               messages.success(request,"Login Successful")
               return redirect("/")  
            else:
                messages.error(request,"Yor are not register")
                return redirect("/register")             
    return render(request,'fnlogin.html')

def fnlogout(request):
    logout(request)
    messages.success(request,"Logout")
    return redirect('/')   

def profile(request):
    if request.user.is_authenticated:
        todos=Todo.objects.filter(user=request.user,isfinished=False)
        homework=Homework.objects.filter(user=request.user,isfinished=False)
        if len(todos)==0:
           tododone=True
        else:
           tododone=False
       
        if len(homework)==0:
           homework_done=True
        else:
           homework_done=False
        context={"todos":todos,"tododone":tododone,"homework":homework,"homework_done":homework_done}
        return render(request,'profile.html',context)
    else:
        messages.warning(request,"Have to Login to see profile")
        return redirect('/')

def calculation(request):
    if request.method=="POST":
        values=request.POST['values']      
        try:
           result=eval(values)
           context={'result':result,'values':values}
           return render(request,'calculation.html',context)
        except: 
           print("exceptioon occure")
           context={'result':"",'values':""}
           return render(request,'calculation.html',context)
    return render(request,'calculation.html')
    

    
