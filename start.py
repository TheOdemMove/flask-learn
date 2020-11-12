from flask import Flask, render_template, request, url_for, redirect
from ldap3 import Server, Connection
#from flask_sslify import SSLify
import random

#import ssl
#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#context.load_cert_chain('/home/admin21/studycisco_server.pem', '/home/admin21/studycisco_server.key')
#context = SSL.Context(SSL.PROTOCOL_SSLv23)
#context.use_privatekey_file('/home/admin21/studycisco_server.key')
#context.use_certificate_file('/home/admin21/studyciso_server.pem')



def addusr(chatid, phone, email, login, psw, name, surname, gnum, bday, posada):
    # pager - chatid от телеграма
    # mobile - номер телефону
    # mail - просто email
    # cn, uid - логин
    # userPassword - пароль юзера
    # sn = прізвище, ім'я
    # fax - номер групи
    try:
        f = open("count")
        ff = f.read()
        f.close()
        ff = int(ff) + 1
        f = open("count", "w")
        f.write(str(ff))
        f.close()
        usid = ff
    except IOError:
        usid = random.randint(10, 100000)
    oneparam = 'cn='+str(login)+',cn=registration,dc=k21'
    hdir = '/home/'+ str(login)
    fname = str(name) + ' ' + str(surname)

    server = Server('ldaps://ldap.k21', port=636, use_ssl=True)
    conn = Connection(server, user='cn=admin,dc=k21', password='Openadmin21')
    conn.bind()


    conn.add(oneparam, ['inetOrgPerson', 'posixAccount'],
             {'cn': str(login), 'gidNumber': 10, 'homeDirectory': str(hdir), 'sn': str(fname),
              'uid': str(login), 'uidNumber': str(usid), 'loginShell': '/bin/bash', 'userPassword': str(psw),
              'mail' : str(email), 'pager': str(chatid), 'description': str(gnum), 'mobile': str(phone),
              'initials' : str(bday), 'street' : str(posada)})


    #conn.add('cn=TheOdemMove,cn=registration,dc=k21', ['inetOrgPerson', 'posixAccount'],
    #         {'cn': 'TheOdemMove', 'gidNumber': 10, 'homeDirectory': '/home/TheOdemMove', 'sn': 'Volodymyr Haryachyi',
    #          'uid': 'TheOdemMove', 'uidNumber': 8, 'loginShell': '/bin/bash', 'userPassword': '2281337228',
    #          'mail': 'playcastro228@gmail.com', 'pager': '487348303', 'fax': '262', 'mobile': '+380502833421'})
    print(conn.result)
    conn.unbind()


app = Flask(__name__)
#sslify = SSLify(app)


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        addusr(request.form['chatid'], request.form['phone'], request.form['email'], request.form['login'], request.form['psw'], request.form['name'], request.form['surname'], request.form['number'], request.form['birthday'], request.form['posada'])
        # виклик функції створення користувача в ldap
        return redirect('/register')
    return render_template('index.html')


@app.route('/register')
def succ():
    return render_template('succ.html')



if __name__ == '__main__':
    app.run(debug=True, host="192.168.21.125", port="505", use_reloader=True, ssl_context='adhoc') #ssl_context=('/home/admin21/studycisco_server.pem', '/home/admin21/studycisco_server.key'))
