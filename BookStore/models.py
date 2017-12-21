from django.db import models
from django.contrib.auth.models import User
from django.db import connection

#####Creating Tables With Models#####

class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    intro = models.CharField(max_length=500)
    copy = models.IntegerField(default=0)
    publisher = models.CharField(max_length=50)
    year = models.IntegerField(default=0)
    subject = models.CharField(max_length=50)
    avgrate = models.FloatField(default=0.0)
    
class Feedbacks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE,default='')
    text = models.CharField(max_length=500,default='')
    rate = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    avgrate = models.FloatField(default=0.0)
    
class Feedbackrates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedbacks, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    
class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    copy = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)


#####Creating Tables With Raw SQL#####

#class TableCreation():
#    with connection.cursor() as cursor:
#        cursor.execute('''CREATE Table Authors(
#        name CHAR(64) PRIMARY KEY
#        )''')
#        cursor.execute('''CREATE Table Publishers(
#        name CHAR(64) PRIMARY KEY
#        )''')
#        cursor.execute('''CREATE Table Subjects(
#        name CHAR(64) PRIMARY KEY
#        )''')
#        cursor.execute('''CREATE Table Books(
#        id INT(8) PRIMARY KEY,
#        title CHAR(128),
#        intro CHAR(512),
#        copy INT(4),
#        author CHAR NOT NULL,
#        publisher CHAR NOT NULL,
#        publishyear INT(4),
#        subject CHAR NOT NULL,
#        FOREIGN KEY (author) REFERENCES Authors(name),
#        FOREIGN KEY (publisher) REFERENCES Publishers(name),
#        FOREIGN KEY (subject) REFERENCES Subjects(name)
#        )''')
#        cursor.execute('''CREATE TABLE Feedbacks(
#        username CHAR NOT NULL,
#        bookid INT NOT NULL,
#        booktitle CHAR NOT NULL,
#        text CHAR(512),
#        rate INT(1),
#        date DATE,
#        PRIMARY KEY (username,bookid),
#        FOREIGN KEY (uername) REFERENCES auth_user(username), 
#        FOREIGN KEY (bookid) REFERENCES Book(id),
#        FOREIGN KEY (booktitle) REFERENCES Book(title).
#        ON DELETE CASCADE
#        )''')
#        cursor.execute('''CREATE TABLE Feedbackrates(
#        username CHAR NOT NULL,
#        feedback_username CHAR NOT NULL,
#        feedback_bookid INT NOT NULL,
#        rate INT(1),
#        date DATE
#        PRIMARY KEY (username,feedback_username,feedback_bookid),
#        FOREIGN KEY (uername) REFERENCES auth_user(username),
#        FOREIGN KEY (feedback_username) REFERENCES auth_user(username),
#        FOREIGN KEY (feedback_bookid) REFERENCES Book(id),
#        ON DELETE CASCADE
#        )''')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
