import os
from flask import Flask, redirect, render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from random import *
import mysql.connector
import re
from pyparsing import dict_of
from werkzeug.utils import secure_filename
from chatbot import chatbot
import random
# <----------------------------------->
# DATABASE CONNECTION
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="pythonproject"
)
# <----------------------------------->
# APP CONNECTOR
app = Flask(__name__)
# <----------------------------------->
# MAIL CONNECTOR
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'cm.b.49ayush.shukla@gmail.com',
    MAIL_PASSWORD = 'ayusshh19'
)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
mycursor = mydb.cursor()
mail = Mail(app)
# <----------------------------------->
# FOR OTP
otp=randint(1000,9999)
# <----------------------------------->
# CONTACT US FORM
@app.route("/",methods = ['GET', 'POST'])
def hello():
    if(request.method=='POST'):
        '''Add entry to the database'''
        fname1 = request.form.get('fname')
        lname1 = request.form.get('lname')
        email1 = request.form.get('email')
        sub1= request.form.get('subject')
        message1 = request.form.get('message')
        sql = "INSERT INTO contact (first, last,email,subject,message) VALUES (%s, %s,%s,%s,%s)"
        val = (fname1, lname1,email1,sub1,message1)
        mycursor.execute(sql, val)

        mydb.commit()

        mail.send_message('New message from {}'.format(fname1),
    sender = email1,
    recipients = ["cm.b.49ayush.shukla@gmail.com"],
    body = message1,
    )
    return render_template('index.html')
# <----------------------------------->
# REGISTER FORM
@app.route("/register")
def register():
    return render_template("register.html",errormessage=False)

# <----------------------------------->
# LOGIN FORM
@app.route("/login",methods = ['GET', 'POST'])
def login():
    return render_template("login.html")
# <----------------------------------->
list_rand=[]
# AFTER LOG IN SUBMIT
@app.route("/loginfetch",methods = ['GET', 'POST'])
def loginfetch():
    if(request.method=='POST'):
        email1 = request.form.get('email')
        pass1 = request.form.get('pass')
        sql = f"select username,profilepic from profile where username=(SELECT username FROM registration WHERE email='{email1}' and password1='{pass1}')"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        print(myresult)
        if len(myresult)>0:
            session['name']=myresult[0][0]
            session['filename']=myresult[0][1]
            rand_number=random.randint(16,21)
            list_rand.append(rand_number)
            print(session['name'])
            print(rand_number)
            sql = f"SELECT * FROM profile WHERE `sr.no`='{rand_number}'"
            mycursor.execute(sql)
            mynew_result = mycursor.fetchall()
            print(mynew_result)
            if len(mynew_result)>0:
                sql =f"update profile set visit=visit+1 where `sr.no`='{rand_number}'"
                mycursor.execute(sql)
            dict_profile={
                'name':session['name'],
                'data':mynew_result,
                'filename':session['filename']
            }
            return render_template("jackport.html",name=dict_profile)
        else:
            return render_template("login.html")
list_register=[]
# <----------------------------------->
# AFTER OTP SUBMIT
@app.route("/otp",methods = ['GET', 'POST'])
def verify_otp():
    if(request.method=='POST'):
        '''Add entry to the database'''
        in1 = request.form.get('input1')
        in2 = request.form.get('input2')
        in3 = request.form.get('input3')
        in4 = request.form.get('input4')
        otp_user=int(in1+in2+in3+in4)
        if otp==otp_user:
            sql = "INSERT INTO registration (username,email,password1) VALUES (%s, %s,%s)"
            val = (list_register[0][1], list_register[0][0],list_register[0][2])
            mycursor.execute(sql, val)
            mydb.commit()
            print(list_register)
            session['name']=list_register[0][1]
            session['email']=list_register[0][0]
            list_register.clear()
            return render_template("profile.html",content={'name':session['name'],'email':session['email']})
        else:
            return render_template("register.html")
# <----------------------------------->            
# AFTER REGISTRATION SUBMIT
@app.route("/registration",methods = ['GET', 'POST'])
def sigup():
    email1 = request.form.get('email')
    user1 = request.form.get('username')
    pass1 = request.form.get('pass')
    repass1 = request.form.get('repass')
    x = re.search("[A-Z][a-z]{4}[0-9]{3}", user1)
    y = re.search('[A-Z][a-z].+[0-9].+', pass1)
    z = re.search('[cm]{2}\.[ab]+\.[0-9].[A-Za-z.].+\@', email1)
    if x:
        errormessage=False
    else:
        errormessage=True
    if y:
        errorpass=False
    else:
        errorpass=True
    if z:
        erroremail=False
    else:
        erroremail=True
    if pass1==repass1 and errorpass==False and erroremail==False and errormessage==False:    
        list_register.append([email1,user1,pass1])
        mail.send_message('Your OTP:',
        sender = "cm.b.49ayush.shukla@gmail.com",
        recipients = [email1],
        body = "Your OTP is {}".format(otp),
        )
        return render_template("otp.html",email=email1)
    else:
        errorobj={
            "erroremail":erroremail,
            "errormessage":errormessage,
            "errorpass":errorpass}
        
        return render_template("register.html",errormessage=True)
# <----------------------------------->    
# AFTER QUIZ FORM SUBMIT
@app.route("/quiz",methods = ['GET', 'POST'])
def quiz():
    if(request.method=='POST'):
        nature=request.form.get("nature")
        mess=request.form.get("mess")
        friends=request.form.get("friends")
        type=request.form.get("type")
        print(session['name'])
        user=session['name']
        print(user)
        print(mess,friends,type,user)
        sql = "INSERT INTO personal_quality(username,nature,mess,friends,type) VALUES (%s,%s,%s,%s,%s)"
        val = (user,nature,mess,friends,type)
        mycursor.execute(sql, val)
        mydb.commit()
        rand_number=random.randint(10,30)
        list_rand.append(rand_number)
        print(rand_number)
        sql = f"SELECT * FROM profile  WHERE `sr.no`='{rand_number}'"
        mycursor.execute(sql)
        mynew_result = mycursor.fetchall()
        if len(mynew_result)>0:
            sql =f"update profile set visit=visit+1 where `sr.no`='{rand_number}'"
            mycursor.execute(sql)
            
        print(mynew_result)
        dict_profile={
            'name':user,
            'data':mynew_result,
            'filename':session['filename']
        }
        print(dict_profile['data'])
        return render_template("jackport.html",name=dict_profile)
    
@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")   

# profile managements
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/profile",methods = ['GET', 'POST'])
def profile1():
    if request.method=='POST':
        if 'file' not in request.files:
            return render_template('quiz.html', filename=filename)
        file = request.files['file']
        if file.filename == '':
            return render_template('quiz.html', filename=filename)
        if file and allowed_file(file.filename):
            fname= request.form.get("name")
            sname= request.form.get("surname")
            mob = request.form.get("mob")
            address= request.form.get("address")
            State= request.form.get("state")
            education = request.form.get("education")
            country= request.form.get("country")
            print(session['name'])
            bio=request.form.get("bio")
            instagram=request.form.get("instagram")
            username= session['name']
            filename = secure_filename(file.filename)
            session['filename']=filename
            print(filename)
            profilepic=filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            sql = "INSERT INTO profile(fname,sname,mob,address,state,education,country,profilepic,username,bio,instagram) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (fname,sname,mob,address,State,education,country,profilepic,username,bio,instagram)
            mycursor.execute(sql, val)
            mydb.commit()
            #print('upload_image filename: ' + filename)
            return render_template('quiz.html',content={'name':session['name'],'filename':filename})
        else:
            return render_template('quiz.html', filename=filename)
        
@app.route('/user_detail')
def user():
    print(session['name'][0])
    member_name=session['name']
    sql = f"SELECT * FROM profile inner join personal_quality on profile.username=personal_quality.username WHERE `profile`.`username`='{member_name}';"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for item in myresult:
        print(item)
    myresult=list(myresult)
    print(myresult)
    if len(myresult)>0:
        return render_template("user_detail.html",data=myresult)
    else:
        return render_template("jackport.html")
    
@app.route("/chatbot")
def home():
    return render_template("chatbot.html",userimage=session['filename'])

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))

@app.route("/new_member_profile")
def new_mem_prof():
    print(list_rand[0])
    new_ran=list_rand[0]
    sql = f"SELECT * FROM profile inner join personal_quality on profile.username=personal_quality.username WHERE `profile`.`sr.no`='28';"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    list_rand.clear()
    myresult=list(myresult)
    print(myresult)
    if len(myresult)>0:
        return render_template("user_detail.html",data=myresult)
    else:
        return render_template("jackport.html")
app.run(debug=True)