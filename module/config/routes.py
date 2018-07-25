from module import app
from module.controllers.logins import Logins

logins = Logins()

@app.route("/")
def index():
    return logins.index()


@app.route("/register", methods=['POST'])
def register():
    return logins.register()

#not built yet
@app.route("/login", methods=['POST'])
def login():
    return logins.login()


#not built yet
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return logins.logout()


@app.route('/create_mess', methods=['POST'])
def send():
    return logins.send()



@app.route("/delete", methods = ['POST'])
def delete():
    return logins.delete()


@app.route("/success")
def success():
    return logins.success()

