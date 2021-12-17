import json
import random
import os
from operator import is_not
from re import search
from flask import Flask
from flask.templating import render_template
from flask_mysqldb import MySQL
from flask import request
from flask import redirect,url_for,session,flash,escape,jsonify
from datetime import datetime, date, timedelta
from pytz import timezone

#Global variables#################################
vuelos = None                                   #
timezones = {"LONDRES" : "Europe/London",       #
        "MADRID" : "Europe/Madrid",             #
        "NEW YORK" : "America/New_York",        #
        "BUENOS AIRES" : "America/Buenos_Aires"}#
dfmt = '%Y-%m-%d %H:%M'
#################################################
 

#Configuramos nuestra aplicacion para que pueda ser conectada a la base de datos
app = Flask (__name__)
#app.config['MYSQL_HOST'] = 'us-cdbr-east-05.cleardb.net'
#app.config['MYSQL_USER'] = 'bdbb92f1a17fd3'
#app.config['MYSQL_PASSWORD'] = '3044d49f'
#app.config['MYSQL_DB'] = 'heroku_371e86085175bc4'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'venta_tiquetes'
mysql = MySQL(app)


#Arreglo RunTimeError
app.secret_key = 'encodekey'

#Pagina Principal
@app.route('/')
def index():
    return render_template('index.html')

#Funcionalidad del cierre de sesion
@app.route('/logout')
def logout():
        session.clear()
        return redirect(url_for('index'))


##@socketio.on('message')

#Pagina de registro-------------------------------------------------------------------------------------------------
@app.route('/register')
def register():
        return render_template('register.html')

#Registrando e ingresando usuario a la base de datos
@app.route('/registered', methods = ['POST'])
def registered():
        if request.method == 'POST':
             # por medio de request.form se trae los datos que introdujo el usuario
             IDusuario = request.form['identificacion-usuario']   
             Nombres = request.form['nombres'] 
             Apellidos = request.form['apellidos']
             IDSexo = request.form['inputSex']
             FechaNacimiento = request.form['fechaNacimiento']
             LugarNacimiento = request.form['lugarNacimiento']    
             Email = request.form['correoE']
             DireccionFacturacion = request.form['dFacturacion']
             Telefono = request.form['telefono'] 
             Contraseña = request.form['pass'] 
             ConfirmarContraseña = request.form['passC']
             #Si el usuario escribio bien la contraseña y su confirmacion este usuario podra ser creado si ya no esta registrado
             if Contraseña == ConfirmarContraseña:
                cur = mysql.connection.cursor()
                cur.execute("SELECT Email,IDusuario FROM `usuario` WHERE Email = '%s' OR IDusuario = '%s'" % (Email,IDusuario))
                data = cur.fetchall()
                print(data)
                if data == ():
                        cur.execute("""INSERT INTO usuario (IDusuario,Nombres,Apellidos,IDtipoUsuario,FechaNacimiento,LugarNacimiento,Email,IDSexo,DireccionFacturacion,Telefono,Contraseña)
                                VALUES (%s,%s,%s,1,%s,%s,%s,%s,%s,%s,%s)""",(IDusuario,Nombres,Apellidos,FechaNacimiento,LugarNacimiento,Email,IDSexo,DireccionFacturacion,Telefono,Contraseña))
                        mysql.connection.commit()
                        return render_template('registered.html')
             #Si el usuario pone diferente las contraseñas le mostrara lo alertara con un error y lo mandara nuevamente a la pagina 
                else:
                        flash('Identificacion o Usuario ya han sido registrados')
                        return render_template('register.html')
             else:
                     return render_template('register.html')  
#-------------------------------------------------------------------------------------------------------------------

#Login
@app.route('/login')
def login(): 
        return render_template('login.html')

#Redireccionar Usuario
@app.route('/logined', methods = ['POST'])
def logined():
        if request.method == 'POST':
                Email = request.form['email']
                Contraseña = request.form['password']
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM `usuario` WHERE Email = '%s'" % (Email))
                logindata = cur.fetchone()
                print(logindata)
                if  logindata != None and Contraseña == logindata[10]:
                        if logindata[3] == 1:
                                session['user'] = logindata[0]
                                return redirect(url_for('indexSession'))
                        else:
                                session['admin'] = Email
                                return redirect(url_for('admin'))
                else:
                        flash('Contraseña o usuario incorrecto')
                        return redirect(url_for('login'))
        return 'bad request'

#Pagina principal del usuario registrado
@app.route('/session')
def indexSession():
        if 'user' in session:
                return render_template('indexSession.html')
        else:
                return render_template('index.html')

#pagina del admin
@app.route('/admin')
def admin():
        if 'admin' in session:
                return render_template('admin.html')
        else:
                return render_template('index.html')

############################################################## PAGINAS USUARIO ######################################
#Menu Usario - Mis viajes
@app.route('/userflight')
def userflight():
        if 'user' in session:
                print(session['user'])
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM `usuario` WHERE IDusuario = '%s'" % (session['user']))
                logindata = cur.fetchone()
                return render_template('profile_flightHistory.html',informacion = logindata)
        else:
                return render_template('index.html')

#Menu Usuario - Check In
@app.route('/usercheckin')
def usercheckin():
        if 'user' in session:
                print(session['user'])
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM `usuario` WHERE IDusuario = '%s'" % (session['user']))
                logindata = cur.fetchone()
                return render_template('profile_check-in.html',informacion = logindata)
        else:
                return render_template('index.html')

#Menu Usuario - Agregar Monto
@app.route('/addamount')
def addamount():
        if 'user' in session:
                print(session['user'])
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM `usuario` WHERE IDusuario = '%s'" % (session['user']))
                logindata = cur.fetchone()
                return render_template('profile_addAmount.html',informacion = logindata)
        else:
                return render_template('index.html')

#Menu Usuario - Agregar Tarjeta
@app.route('/addcard')
def addcard():
        if 'user' in session:
                print(session['user'])
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM `usuario` WHERE IDusuario = '%s'" % (session['user']))
                logindata = cur.fetchone()
                return render_template('profile_addCard.html',informacion = logindata)
        else:
                return render_template('index.html')

#Menu Usuario - Edit
@app.route('/useredit')
def useredit():
        if 'user' in session:
                print(session['user'])
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM `usuario` WHERE IDusuario = '%s'" % (session['user']))
                logindata = cur.fetchone()
                return render_template('profile_edit.html',informacion = logindata)
        else:
                return render_template('index.html')
######################################################################################################################

############################################################### FUNCIONALIDADES USUARIO #############################

#Editar Email
@app.route('/emailedit', methods = ['POST'])
def emailedit():
        newEmail = request.form['nemail']
        id = session['user']
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE usuario 
                        SET Email = %s
                        WHERE IDusuario = %s""", (newEmail,id))
        mysql.connection.commit()
        return redirect(url_for('indexSession'))

#Editar Correo
@app.route('/directionedit', methods = ['POST'])
def directionedit():
        newDirection = request.form['ndirection']
        id = session['user']
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE usuario 
                        SET DireccionFacturacion = %s
                        WHERE IDusuario = %s""", (newDirection,id))
        mysql.connection.commit()
        return redirect(url_for('indexSession'))

#Editar Contraseña
@app.route('/passwordedit', methods = ['POST'])
def passwordedit():
        oldPass = request.form['oldpassword']
        newPass = request.form['newpassword']
        newPass2 = request.form['newpassword2']
        id = session['user']
        cur = mysql.connection.cursor()
        cur.execute("SELECT Contraseña FROM usuario WHERE IDusuario = '%s' " % (id))
        passfound = cur.fetchone()
        if passfound[0] == oldPass:
                if newPass == newPass2:
                        cur = mysql.connection.cursor()
                        cur.execute("""UPDATE usuario 
                                        SET Contraseña = %s
                                        WHERE IDusuario = %s""", (newPass,id))
                        mysql.connection.commit()
                        return redirect(url_for('indexSession'))
                else:
                        flash('Las contraseñas no son las mismas')
                        return redirect(url_for('useredit'))
        else:
                flash('Contraseña actual incorrecta')
                return redirect(url_for('useredit'))

#Agregar Tarjeta
@app.route ('/newcreditcard',methods = ['POST'])
def newcreditcard():
        Numbercard = request.form['NumberT']
        Month = request.form['Month']
        Year = request.form['Year']
        Ccv = request.form['Ccv']
        NameOwner = request.form['CardName']
        id = session['user']
        cur = mysql.connection.cursor()
        cur.execute("SELECT IDTarjeta FROM `modulofinanciero` WHERE IDTarjeta = '%s' " % (Numbercard))
        data = cur.fetchall()
        if data == ():
                cur.execute("""INSERT INTO modulofinanciero (IDTarjeta,MesVencimiento,AñoVencimiento,Ccv,NombreTitular,Dinero,IDusuario)
                                VALUES (%s,%s,%s,%s,%s,0,%s)""", (Numbercard,Month,Year,Ccv,NameOwner,id))
                mysql.connection.commit()
                return redirect(url_for('indexSession'))
        else:
                flash('Tarjeta ya registrada')
                return redirect(url_for('addcard'))


if __name__ == '__main__':
        app.run(debug=True, port=5000)
        