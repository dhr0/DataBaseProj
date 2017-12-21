from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from .models import Books
from .models import Feedbacks
from .models import Feedbackrates
from .models import Orders
import numpy as np

def index(request):
    return render(request, 'index.html')
    
def login(request):
    return render(request, 'login.html')
    
## user authentication function ##
def trylogin(request):
    username = request.GET['user']
    password = request.GET['password']
    user = authenticate(username=username, password=password)
    if user!=None: 
        auth.login(request,user)
        return render(request, 'successlogin.html', context = {"username":username})
    else:
        return HttpResponse("Incorrect username or password")

def regist(request):
    return render(request, 'regist.html')
    
## user registration function ##
def tryregist(request):
    username = request.GET['user']
    password = request.GET['password']
    cpassword = request.GET['cpassword']
    ## check username and password, error messages return##
    if len(username)>30:
        return render(request, 'unsuccessregist.html', context = {"error":"username over 30 characters"}) 
    elif len(username)==0:
        return render(request, 'unsuccessregist.html', context = {"error":"username cannot be blank"}) 
    elif len(password)>30:
        return render(request, 'unsuccessregist.html', context = {"error":"password over 30 characters"})
    elif len(password)==0:
        return render(request, 'unsuccessregist.html', context = {"error":"password cannot be blank"})
    elif password!=cpassword:
        return render(request, 'unsuccessregist.html', context = {"error":"confirm password doesn't match"})
    count = 0
    for i in User.objects.raw("SELECT id from auth_user WHERE username = %s",[username]):
        count += 1
    if count:
        return render(request, 'unsuccessregist.html', context = {"error":"username already exist"})
    else:
        ## create new user ##
        user = User.objects.create_user(username,"",password)
        #####Raw SQL#####
        #with connection.cursor() as cursor:
        #cursor.execute("INSERT INTO auth_user (password,username) Values('%s','%s')"%(password,username))
        user.save()
        return HttpResponse("Welcome!")
     
## user message page ##
def user(request):
    ## search for order history ##
    orderlist = Orders.objects.raw("SELECT * from BookStore_Orders WHERE user_id = '%s'"%(request.user.id))
    ## search for feedback history ##
    feedbacklist = Feedbacks.objects.raw("SELECT * from BookStore_Feedbacks WHERE user_id = '%s'"%(request.user.id))
    ## search for feedback uselfulness rating history ##
    feedbackratelist = Feedbackrates.objects.raw("SELECT * from BookStore_Feedbackrates WHERE user_id = '%s'"%(request.user.id))
    return render(request, 'user.html', context = {"c_user":request.user,"orderlist":orderlist,"feedbacklist":feedbacklist,"feedbackratelist":feedbackratelist})
    
  
## admin page ##
def useradmin(request):
    return render(request, 'useradmin.html', context = {"user":request.user})

def newbook(request):
    yearlist=[]
    for i in range (1800,2018):
        yearlist+=[i]
    return render(request, 'newbook.html',context = {"yearlist":yearlist})

## add in new books ##
def trynewbook(request):
    title = request.GET['title']
    ## check inputs, error messages return ##
    if len(title)>100:
        return render(request, 'unsuccessnewbook.html', context = {"error":"title over 100 characters"})
    elif len(title)==0:
        return render(request, 'unsuccessnewbook.html', context = {"error":"title cannot be blank"})
    count = 0
    for i in Books.objects.raw("SELECT id from BookStore_Books WHERE title = %s",[title]):
        count += 1
    if count:
        return render(request, 'unsuccessnewbook.html', context = {"error":"book already exist"})
    author = request.GET['author']
    if len(author)>50:
        return render(request, 'unsuccessnewbook.html', context = {"error":"author over 50 characters"})
    elif len(author)==0:
        return render(request, 'unsuccessnewbook.html', context = {"error":"author cannot be blank"})
    publisher = request.GET['publisher']
    if len(publisher)>50:
        return render(request, 'unsuccessnewbook.html', context = {"error":"publisher over 50 characters"})
    elif len(publisher)==0:
        return render(request, 'unsuccessnewbook.html', context = {"error":"publisher cannot be blank"})
    year = request.GET['year']
    subject = request.GET['subject']
    if len(subject)>50:
        return render(request, 'unsuccessnewbook.html', context = {"error":"subject over 50 characters"})
    elif len(subject)==0:
        return render(request, 'unsuccessnewbook.html', context = {"error":"subject cannot be blank"})
    intro = request.GET['intro']
    if len(intro)>500:
        return render(request, 'unsuccessnewbook.html', context = {"error":"intro over 500 characters"})
    elif len(intro)==0:
        return render(request, 'unsuccessnewbook.html', context = {"error":"intro cannot be blank"})
    ## create new book ##
    Books.objects.create(title=title,author=author,intro=intro,publisher=publisher,year=int(year),subject=subject)
    #####Raw SQL#####
    #with connection.cursor() as cursor:
    #cursor.execute("INSERT INTO BookStore_Books VALUES ('%s','%s','%s',0,'%s',%s,'%s')",[title,author,intro,publisher,year,subject])
    return HttpResponse("Success")
   
def newcopy(request):
    booklist = []
    for book in Books.objects.raw("SELECT id,title from BookStore_Books"):
        booklist += [book]
    copylist=[]
    for i in range (0,101):
        copylist+=[i]
    return render(request, 'newcopy.html', context = {"booklist":booklist,"copylist":copylist})

## arrival of new copies ##    
def trynewcopy(request):
    b_id = request.GET['id']
    copy = request.GET['copy']
    ## increase copy number of selected book ##
    with connection.cursor() as cursor:
        cursor.execute("UPDATE BookStore_Books SET copy = copy + %s WHERE id = '%s'"%(copy,b_id))
    return HttpResponse("Copy Added")
 
## keyword searching ##
def browsing(request):
    keyword = request.GET['keyword']
    sort = request.GET['sort']
    ## search for books with input keyword ##
    booklist = Books.objects.raw("SELECT * FROM BookStore_Books WHERE title LIKE '%%%s%%' OR author LIKE '%%%s%%' OR intro LIKE '%%%s%%' OR publisher LIKE '%%%s%%' ORDER BY %s DESC"%(keyword,keyword,keyword,keyword,sort))
    return render(request, 'browsing.html', context = {"booklist":booklist})

## book detail page ##
def book(request):
    b_id = request.GET['id']
    ## get messages of the book ##
    b = Books.objects.raw("SELECT * from BookStore_Books WHERE id = '%s'"%(b_id))[0]
    copylist=[]
    for i in range (0,b.copy+1):
        copylist+=[i]
    ratelist=[]
    for i in range (0,11):
        ratelist+=[i]
    ## get feedbacklist of the book ##
    feedbacklist = Feedbacks.objects.raw("SELECT * FROM BookStore_Feedbacks WHERE book_id=%s"%(b_id))
    return render(request, 'book.html', context = {"book":b,"copylist":copylist,"ratelist":ratelist,"feedbacklist":feedbacklist})

## order function and book recommendation ##
def order(request,b_id):
    copy = request.GET['copy']
    ## decrease the copy number ##
    with connection.cursor() as cursor:
        cursor.execute("UPDATE BookStore_Books SET copy = copy - %s WHERE id = '%s'"%(copy,b_id))
    b = Books.objects.raw("SELECT * from BookStore_Books WHERE id = '%s'"%(b_id))[0]
    ## create a new order ##
    Orders.objects.create(user=request.user,book=b,copy=copy)
    #####Raw SQL#####
    #with connection.cursor() as cursor:
    #cursor.execute("INSERT INTO BookStore_Orders (user_id,book_id,copy) VALUES (%s,%s,%s)"%(request.user.id,b_id,copy))
    norecommendation = False
    with connection.cursor() as cursor:
        ## search for books that other users also buy ##
        cursor.execute("SELECT DISTINCT book_id FROM BookStore_Orders WHERE user_id IN(SELECT DISTINCT user_id FROM BookStore_Orders WHERE book_id=%s) AND book_id != %s AND user_id != %s"%(b_id,b_id,request.user.id))
        booklist = cursor.fetchone()
        if booklist is not None:
            recommendationlist=[([0]*2)for i in range(len(booklist))]  
            count=0
            for book in booklist:
                ## calculate total sells for the booklist ##
                cursor.execute("SELECT SUM(copy) FROM BookStore_Orders WHERE book_id=%s AND user_id IN(SELECT DISTINCT user_id FROM BookStore_Orders WHERE book_id=%s) AND user_id != %s"%(str(book),b_id,request.user.id))
                recommendationlist[count][0] = int(book)
                recommendationlist[count][1] = cursor.fetchone()[0]
                count += 1
            ## list sorting ##
            sortdata=np.array(recommendationlist)
            idex=np.lexsort([-1*sortdata[:,1]])
            recommendationlist = sortdata[idex, :]
            data=[]
            ## generate recommendation list ##
            for i in range(0,len(booklist)):
                data += Books.objects.raw("SELECT * from BookStore_Books WHERE id = '%s'"%(recommendationlist[i][0]))
        else: 
            norecommendation = True     
    if norecommendation: 
        return render(request, 'order.html')
    else:
        return render(request, 'order.html', context = {"booklist":data})
  
## feedback funciton ##
def feedback(request,b_id):
    text = request.GET['feedback']
    rate = request.GET['rate']
    count = 0
    ## check if user has already rated the book ##
    for feedback in Feedbacks.objects.raw("SELECT * from BookStore_Feedbacks WHERE book_id=%s AND user_id=%s"%(b_id,request.user.id)):
        count += 1
    if count:
        return HttpResponse("You have already rated for this book")
    b = Books.objects.raw("SELECT * from BookStore_Books WHERE id = '%s'"%(b_id))[0]
    ## create new feedback ##
    Feedbacks.objects.create(user=request.user,book=b,text=text,rate=rate)
    #####Raw SQL#####
    #with connection.cursor() as cursor:
    #cursor.execute("INSERT INTO BookStore_Feedbacks (user_id,book_id,text,rate) VALUES (%s,%s,'%s',%s)"%(request.user.id,b_id,text,rate))
    count=0
    avgrate=0.0
    ## update averagerate of book##
    for f in Feedbacks.objects.raw("SELECT * FROM BookStore_Feedbacks WHERE book_id=%s"%(b_id)):
        avgrate += f.rate
        count += 1
    avgrate = round(avgrate / count, 2)
    with connection.cursor() as cursor:
        cursor.execute("UPDATE BookStore_Books SET avgrate=%s WHERE id = %s"%(avgrate,b_id))
    return HttpResponse("Feedback Uploaded")
   
## feedback usefulness rate funciton ##
def feedbackrate(request,f_id):
    rate = request.GET['rate']
    f = Feedbacks.objects.raw("SELECT * from BookStore_Feedbacks WHERE id = '%s'"%(f_id))[0]
    ## user cannot rate its own feedback ##
    if f.user.id==request.user.id:
        return HttpResponse("You cannot rate your own feedback")
    count = 0
    ## check if user has already rated the book ##
    for feedbackrate in Feedbackrates.objects.raw("SELECT * from BookStore_Feedbackrates WHERE user_id=%s AND feedback_id=%s"%(request.user.id,f_id)):
        count += 1
    if count:
         return HttpResponse("You have already rated for this feedback")
    ## create new feedback usefulness rate ##
    Feedbackrates.objects.create(user=request.user,rate=rate,feedback=f)
    #####Raw SQL#####
    #with connection.cursor() as cursor:
    #cursor.execute("INSERT INTO BookStore_Feedbackrates (user_id,rate,feedback_id) VALUES (%s,%s,%s)"%(request.user.id,rate,f.id))
    count=0
    avgrate=0.0
    ## update average rate of the feedback ##
    for f in Feedbackrates.objects.raw("SELECT * FROM BookStore_Feedbackrates WHERE feedback_id=%s"%(f_id)):
        avgrate += f.rate
        count += 1
    avgrate = round(avgrate / count, 2)
    with connection.cursor() as cursor:
        cursor.execute("UPDATE BookStore_Feedbacks SET avgrate=%s WHERE id = %s"%(avgrate,f_id))
    return HttpResponse("Rating Uploaded")

## top feedbacks view ##    
def topfeedback(request,b_id,t):
    top=int(t);
    ## search for top t feedbacks ##
    feedbacklist = Feedbacks.objects.raw("SELECT * FROM BookStore_Feedbacks WHERE book_id=%s ORDER BY avgrate DESC"%(b_id))[0:top]
    return render(request, 'topfeedback.html', context = {"book":b_id,"feedbacklist":feedbacklist})
    
    
    
    
