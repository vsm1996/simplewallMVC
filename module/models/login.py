from flask import session, request, flash
from module.config.mysqlconnection import connectToMySQL
from module import app
from flask_bcrypt import Bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

bcrypt = Bcrypt(app)

app.secret_key = "lolgoodluckbud112210!"

mysql = connectToMySQL('simplewall')



class Login():
    def index(self):
        return True
    

    def register(self):
        if len(request.form['first_name']) < 1:
            flash("First name cannot be blank!", 'firstname')
        elif len(request.form['first_name']) <= 2:
            flash("First name must be 2+ characters", 'firstname')
        elif request.form['first_name'].isalpha() == False:
            flash(u"Numbers cannot be in your first name", 'firstname')

        if len(request.form['last_name']) < 1:
            flash("Last name cannot be blank!", 'lastname')
        elif len(request.form['last_name']) <= 2:
            flash("Last name must be 2+ characters", 'lastname')
        elif request.form['last_name'].isalpha() == False:
            flash(u"Numbers cannot be in your last name", 'lastname')
        
        
        query = "SELECT email from users where email = %(email)s"
        
        data = {
            'email': request.form['email']
        }
    
        email_list = mysql.query_db(query, data)
        print("This is email list: ", len(email_list))
        
        if len(request.form['email']) < 1:
            flash("Email cannot be blank!", 'email')
        elif not EMAIL_REGEX.match(request.form['email']):
            flash("Invalid Email Address!", 'email')
        
        elif len(email_list) > 0:
            flash("That email already exists!", 'email')
        
        
        if len(request.form['password']) < 1:
            flash("Password cannot be blank!", 'password')
        elif len(request.form['password']) < 7:
            flash("Password must be 8 or more characters", 'password')
        
        if len(request.form['pwconfirm']) < 1:
            flash(u"This field is required", 'pwconfirm')
        elif request.form['pwconfirm'] != request.form['password']:
            flash(u"Please make sure both password entries are the same.", 'pwconfirm')
            
                
        self.debugHelp("REGISTER METHOD")
        if '_flashes' in session.keys():
            return False
        else:
            pw_hash = bcrypt.generate_password_hash(request.form["password"])
            
            flash("You've been successfully registered, ", request.form['first_name'])

            query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s,%(email)s, %(password)s, NOW(), NOW());"
                    
            data = {
                'first_name' : request.form['first_name'],
                'last_name' : request.form['last_name'],
                'email' : request.form['email'],
                'password' : pw_hash
            }

            session['user_id'] = mysql.query_db(query, data)

            print('ID IS: ', session['user_id'])

            query = "SELECT first_name FROM USERS WHERE email = %(email)s"
            data = {
                'email': request.form['email']
            }

            get_name = mysql.query_db(query, data)

            session['first_name']=get_name[0]['first_name']



            print('NAME IS: ', session['first_name'])


            session['logged_in'] = True
            return True



    def login(self):
        query = "SELECT * FROM USERS where email = %(email)s"

        data = {
            'email' : request.form['elog']
        }


        email_check = mysql.query_db(query, data)

        print("This is email check: ", email_check)

        if email_check:
            if bcrypt.check_password_hash(email_check[0]['password'], request.form['plog']):
                session['logged_in'] = True
                session['first_name'] = email_check[0]['first_name']
                session['user_id'] = email_check[0]['id']
                flash("You successfully logged in...", 'login')

                return True

        session['logged_in'] = False
        flash("Please try again.", 'login')
        
        self.debugHelp("LOGIN METHOD")
        if '_flashes' in session.keys():
            return False


    def logout(self):
        session['logged_in'] = False
        flash("You have been logged out... ")
        return True
        


    def send(self):
        print("YEEET: ", request.form['message'])
        if  len(request.form['message']) <= 1:
            flash("This field is required", 'posted')
        elif len(request.form['message']) > 140:
            flash("Message must be 140 characters or less", 'posted')

        self.debugHelp("SEND METHOD")
        if '_flashes' in session.keys():
            return False
            
        else:
            print("HERE IS FORM:", request.form)

            query = "INSERT INTO messages (content, user_id, receiver_id, created_at, updated_at) VALUES (%(content)s, %(user_id)s, %(receiver_id)s, NOW(), NOW());"
            data = {
            'content': request.form['message'],
            'user_id': session['user_id'],
            'receiver_id':  request.form['hiddenid']
            }
            sent = mysql.query_db(query, data)

            query = "SELECT content from messages"
            
            sentmessage = mysql.query_db(query)
            print("YOUR MESSAGE HERE: ", sentmessage)
            
            return True

    def delete(self):
        query = "DELETE FROM messages WHERE id = %(id)s"
        data = {
            'id' : request.form['delid']
        }
        delete = mysql.query_db(query, data)
        print("DELETED: ", delete)
        return True


    def success(self):
        if session['logged_in'] == False:
            flash("You are not logged in, please login or register.", 'login')
            return False
        else:
            query = "SELECT * from users where id <> %(id)s"
            data = {
                'id' : session['user_id']
            }
            
            get_others = mysql.query_db(query,data)
            if get_others:
                other_users = get_others
                print("AQUI:    ", other_users)
            else:
                
                other_users = ""

            query = "SELECT * FROM messages  JOIN users ON users.id = messages.user_id where receiver_id = %(id)s;"
            data = {
                'id': session['user_id']
            }

            sender_names = mysql.query_db(query,data)

            print ("HERE IS ALL SENDER INFO: ", sender_names)

            all_senders = sender_names
            

            query = "SELECT COUNT(*) from messages where user_id = %(id)s"
            data = {
                'id': session['user_id']
            }
            num_sent = mysql.query_db(query,data)
            session['sent'] = num_sent[0]['COUNT(*)']
            print("AMOUNT OF MESSAGES SENT: ", session['sent'])



            query = "SELECT COUNT(*) from messages where receiver_id = %(id)s"
            data = {
                'id' : session['user_id']
            }
            num_received = mysql.query_db(query,data)

            session['received'] = num_received[0]['COUNT(*)']
            print("AMOUNT OF MESSAGES RECEIVED: ", session['received'])
            return other_users, all_senders

    def debugHelp(self, message = ""):
        print("\n\n-----------------------", message, "--------------------")
        print('REQUEST.FORM:', request.form)
        print('SESSION:', session)
