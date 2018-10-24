from flask import render_template, session, redirect
from module.models.login import Login

login = Login()


class Logins():
    def index(self):
        result1 = login.index()
        return render_template("index.html")
    

    def register(self):
        result2 = login.register()
        if result2 == False:
            return redirect('/')
        else:
            return redirect("/success")


    def login(self):
        result3 = login.login()
        if result3 == True:
                return redirect('/success')
        else:
            return redirect('/')



    def logout(self):
        result4 = login.logout()
        return redirect('/')



    def send(self):
        result5 = login.send()
        if result5 == True:
            return redirect('/success')
            
        else:
            return redirect('/success')




    def delete(self):
        result6 = login.delete()
        print("THIS ONE: ", result6)
        return redirect('/success')
    
    def deletePost(self):
        result7 = login.deletePost()
        print("THIS POST IS BEING DELETED: ", result7)
        return redirect('/success')


    def success(self):
        result8 = login.success()
        print("THIS IS 8: ", result8)
        if result8 == False:
            return redirect('/')
        else:
            return render_template('success.html', name = session['first_name'], users = result8[0], senders = result8[1], posts = result8[2], amountsent = session['sent'], amountreceived = session['received'])
    
    def createPost(self):
        result9 = login.createPost()
        if result9 == True:
            return redirect('/success')
        else: 
            return redirect('/sucess')

