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



    def success(self):
        result7 = login.success()
        print("THIS IS 7: ", result7)
        if result7 == False:
            return redirect('/')
        else:
            return render_template('success.html', name = session['first_name'], users = result7[0], senders = result7[1], amountsent = session['sent'], amountreceived = session['received'])

