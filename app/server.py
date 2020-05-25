from flask import Flask,render_template,request,url_for,redirect,session,flash
import smtplib
# from functools import wraps
from db import *
from passlib.hash import sha256_crypt
from flask_login import current_user, login_user, logout_user
# from functools import wqraps 


app= Flask(__name__)
# conn = connectDB()
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
conn = connectDB()
cursor = conn.cursor(dictionary=True)
global temp
temp = False

def sendmail(message_to_send):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('shubham3962@gmail.com','nATIONAL12')
    to = "shubham7070078010@gmail.com"
    server.sendmail('shubham3962@gmail.com',to,message_to_send)
    server.close()

def send_mail(to, content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('shubham3962@gmail.com','nATIONAL12')
    server.sendmail('shubham3962@gmail.com',to,content)
    server.close()

@app.route("/")
def index():
    return render_template('index.html', val=temp)

@app.route('/about')
def about():
    return render_template('about-us.html', val = temp)

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', val = temp)

@app.route('/contact', methods = ['POST','GET'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html', val = temp)
    if request.method == 'POST':
        contact = request.form
        contact_name = contact['name']
        contact_email = contact['email']
        contact_subject = contact['subject']
        contact_message = contact['message']
        # cursor.execute('insert into donor values(%s,%s,%s,%s) ', (contact_name,contact_email,contact_subject,contact_message))
        content = "There is a mail from \n"+contact_email +"\n" + contact_message
        subject = contact_subject
        message_to_send = 'Subject: {}\n\n{}'.format(subject, content)
        print(message_to_send)
        sendmail(message_to_send)
        return redirect(url_for('contact'))
        
@app.route('/donate', methods = ['POST','GET'])
def donate():
    if request.method == 'GET':
        return render_template('donate.html', val = temp)
    if request.method == 'POST':
        print("HERE IN DONATE")
        donor_details = request.form
        donor_first_name = donor_details['firstname']
        donor_last_name = donor_details['lastname']
        donor_id= donor_details['donorID']
        donor_phone_num = donor_details['phone']
        donor_email = donor_details['email']
        donor_street_add = donor_details['street']
        donor_city = donor_details['city']
        donor_country = donor_details['country']
        donor_amount = donor_details['amount']
        donor_message = donor_details['message']
        print("HERE IN DONATE", donor_amount, donor_city, donor_country, donor_details, donor_email,donor_first_name, donor_id,donor_last_name, donor_message,donor_phone_num,donor_street_add)
        
        cursor.execute('insert into donor values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ', (donor_id, donor_first_name, donor_last_name, donor_phone_num, donor_email, donor_street_add, donor_city, donor_country, donor_amount, donor_message))
    
        conn.commit()
        return redirect(url_for('index'))
@app.route('/sponsor', methods = ['POST','GET'])
def sponsor():
    if request.method == 'GET':
        return render_template('sponsor.html', val = temp)
    if (request.method == 'POST'):
        adopter = request.form
        adopterID = adopter['adopterID']
        animalID=adopter['animalID']
        firstname = adopter['firstname']
        lastname = adopter['lastname']
        phno = adopter['phno']
        email = adopter['email']
        city = adopter['city']
        streetadd = adopter['streetadd']
        country = adopter['country']
        message = adopter['message']
        print(adopterID,firstname,lastname,phno,email,city,streetadd, country, message)
        cursor.execute('insert into adopter values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ', (adopterID,firstname,lastname,phno,email,streetadd,city,country,message,animalID))
        conn.commit()
        #cursor.execute('create trigger test after insert on donor ')
        return redirect(url_for('sponsor'))

@app.route('/sponsorAChild')
def sponser_a_child():
    x= "select * from animalprofile"
    cursor.execute(x)
    res = cursor.fetchall()
    print(res)
    return render_template('sponsor-a-child.html', val = temp, res= res)

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method  == 'GET': 
        return render_template('signup.html')
    if(request.method == 'POST'):
        userdetails = request.form
        username = userdetails['username']
        email = userdetails['email']
        mobile = userdetails['mobile']
        password = userdetails['password']
        confirm_password = userdetails['confirmPassword']
        totdonated = 0
        totadopted = 0

        #print(username, email, password, confirm_password)
        if password != confirm_password:
            return "Password not mathched"
        pwd = sha256_crypt.encrypt(str(password))
        cursor.execute('insert into people values(null, %s,%s,%s,%s,%s,%s) ', (username, email, mobile, pwd, totdonated, totadopted))
        conn.commit()
        val = 'select max(userid) from people'
        result = cursor.execute(val,)
        id = cursor.fetchone()
        id = id['max(userid)']
        val = 'select email from people where userid = {}'.format(id)
        result = cursor.execute(val, )
        email = cursor.fetchone()
        mail_add = email['email']
        content = "Thankyou for joining us. Lets build a wolrd full of humanity.\n" + "This is your User ID: {}".format(id) 
        subject = "PEOPLE FOR ANIMAL"
        message_to_send = 'Subject: {}\n\n{}'.format(subject, content)
        send_mail(mail_add, message_to_send)
        print("mail send")
        return redirect(url_for('index'))
    
    

@app.route("/login", methods = ['POST','GET'])
def login():
    if(request.method  == 'GET'):
        return render_template('login.html')
    if(request.method  == 'POST'):
        userdetails=request.form
        email = userdetails['email']
        password = userdetails['password']
        cursor.execute('select * from people where email = %s', (email,))
        res = cursor.fetchone()
        #print(res)
        if res is None:
            return "Invalid username"
        else:
            pwd = res['password']
            if sha256_crypt.verify(password, pwd):
                # session['logged_in'] == True
                global temp
                temp = True
                #print("this is", temp)
                session['email']= res['email']
                #return 'You are now logged in', 'success'
                return redirect(url_for('index'))

            else:
                return "Invalid password"
    

@app.route("/logout")
def logout():
    global temp
    temp = False
    session.clear()
    return redirect(url_for('index'))



# @app.route("/temp", methods = ['POST', 'GET'])
# def temp():
#     if(request.method == 'GET'):
#         return render_template('temp.html')
#     if(request.method == 'POST'):
#         # print('POST')
#         userdetails = request.form
#         # request.form = {'name': '------',
#         #                   'age': '-----------',
#         #                   'class': '------------------'}
#         # print(userdetails)
#         # for i in userdetails:
#         #     print(i)
#         name = userdetails['name']
#         age = userdetails['age']
#         clas = userdetails['class']
#         st = 'This is temp ' + name + ' ' + age + ' ' + clas
#         # print('This is the req' + st)
#         return st

# @app.route("/temp2", methods = ['POST'])
# def temp2():
#     # if(request.method == 'GET'):
#     #     return render_template('temp.html')
#     if(request.method == 'POST'):
#         # print('POST')
#         userdetails = request.form
#         # request.form = {'name': '------',
#         #                   'age': '-----------',
#         #                   'class': '------------------'}
#         # print(userdetails)
#         # for i in userdetails:
#         #     print(i)
#         name = userdetails['name']
#         age = userdetails['age']
#         clas = userdetails['class']
#         st = 'This is temp2 ' +name + ' ' + age + ' ' + clas
#         # print('This is the req' + st)
#         # qu = "INSERT INTO tableName VALUES('"+ name +"', "+ age +", '"+ clas +"')"
#         # qu = "INSERT INTO tableName VALUES(null, ?, ?, ?)"
#         # sql.query(qu, (name, age, clas))
#         return qu

if __name__ == '__main__':
    app.run()