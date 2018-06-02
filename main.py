#ANSIBLE


import os
import sys
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor



#FLASK

from flask import Flask, request, render_template,redirect,url_for
import mysql.connector
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory

import Models

peticion = 'eliminarCarpeta'
nombre_path = ''
path= "/home/labicsc02-65961/Documentos/"


#clases

class Historial:
    def __init__(self, id, tipoPeticionRealizada, fechaPeticion):
        self.id = id
        self.tipoPeticionRealizada = tipoPeticionRealizada
        self.fechaPeticion = fechaPeticion

    def getId(self):
        return self.id
    def setId(self, nuevo):
        self.id = nuevo

    def getTipopeticionRealizada(self):
        return self.tipoPeticionRealizada
    def setTipoPeticionRealizada(self, nuevo):
        self.tipoPeticionRealizada = nuevo

    def getFechaPeticion(self):
        return self.fechaPeticion
    def setFechaPeticion(self, nuevo):
        self.fechaPeticion = nuevo


class Usuario:
    usuario = None

    def __init__(self, nombreUsuario, contrasenna, rol):
        self.nombreUsuario = nombreUsuario
        self.contrasenna = contrasenna
        self.rol = rol

    def getInstancia(self, nombreUsuario, contrasenna, rol):
        global usuario
        if usuario == None:
            usuario = Usuario(self, nombreUsuario, contrasenna, rol)
            return usuario
        else:
            return usuario




def ansibleFuntion():
    global peticion
    global nombre_path

    loader = DataLoader()


    inventory = InventoryManager(loader=loader, sources='/home/labicsc02-65961/Documentos/Asinble-server/Inventory/inventory')
    variable_manager = VariableManager(loader=loader, inventory=inventory)


    # si lo que se quiere trabajar es un archivo se debe especificar el nombre del file y la extension del file


    if(peticion == 'eliminarCarpeta'):
        playbook_path = '/home/labicsc02-65961/Documentos/Asinble-server/Playbooks/playbook_eliminarCarpeta.yml'

    elif(peticion == 'eliminarArchivo'):
        playbook_path = '/home/labicsc02-65961/Documentos/Asinble-server/Playbooks/playbook_eliminarFile.yml'

    elif(peticion == 'crearArchivoTXT'):
        playbook_path = '/home/labicsc02-65961/Documentos/Asinble-server/Playbooks/playbook_crearArchivoTXT.yml'

    elif(peticion == 'crearCarpeta'):
        playbook_path = '/home/labicsc02-65961/Documentos/Asinble-server/Playbooks/playbook_crearCarpeta.yml'


    if not os.path.exists(playbook_path):
        print('[INFO] The playbook does not exist')
        sys.exit()

    Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax',
                                 'connection','module_path', 'forks', 'remote_user',
                                 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                                 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check','diff'])

    options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False,
                  connection='ssh', module_path=None, forks=100, remote_user='labicsc02-65961',
                  private_key_file='/home/labicsc02-65961/.ssh/id_rsa', ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None,
                  scp_extra_args=None, become=True, become_method='sudo',
                become_user='root', verbosity=None, check=False, diff=False)

    variable_manager.extra_vars = {'hosts': 'all', 'path': nombre_path } # This can accomodate various other command line arguments.`

    passwords = dict(vault_pass='adminlabicssc2018')

    pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=passwords)

    results = pbex.run()



cnx = mysql.connector.connect(user='root', password='123',
                              host='127.0.0.1',
                              database='ansibleBase')

app = Flask(__name__)

#START
#RUTAS DE VISTAS

#------------------------------------------------------------------------------------------


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/obtenerHistorial',methods=['GET','POST'])
def obtenerHistorial():
    lista = []
    session= Models.Session.getInstance()
    nombreUsuario=session.getlogedUser().nombreUsuario

    if request.method == 'GET':
        cursorRegistros = cnx.cursor()
        query = "SELECT h.id, h.tipoPeticionRealizada, h.fechaPeticion " \
                "FROM Historial as h inner join Usuario_Historial as uh " \
                "where h.id=uh.id_historial and uh.nombre_usuario = '" + nombreUsuario + "'"

        cursorRegistros.execute(query)
        fila = cursorRegistros.fetchall()
        for item in fila:
            idHistorial = str(item[0])
            tareaHistorial = str(item[1])
            fechaHistorial = str(item[2])
            historialElement = Historial(idHistorial,tareaHistorial,fechaHistorial)
            lista.append(historialElement)
        #return str(len(fila))
        return render_template('records.html', lista = lista)


@app.route('/index')
def index():
    session = Models.Session.getInstance()
    tipo_usuario = session.getlogedUser().rol
    nombreUsuario = session.getlogedUser().nombreUsuario
    return render_template('index.html', tipo_usuario=tipo_usuario, nombreUsuario=nombreUsuario)



@app.route('/login', methods=['POST'])
def dbLogin():

    user = request.form['email']
    password = request.form['password']

    cursorRegistros = cnx.cursor()
    query = "SELECT * from Usuario"

    cursorRegistros.execute(query)
    fila = cursorRegistros.fetchall()
    for item in fila:

        if str(item[0]) == user and str(item[1]) == password:
            nombreUsuario = str(item[0])
            contrasenna = str(item[1])
            rol = str(item[2])
            session=Models.Session.getInstance()
            usuario =Usuario(nombreUsuario, contrasenna, rol)
            session.logUser(usuario)


            return render_template('index.html',tipo_usuario=rol,nombreUsuario= nombreUsuario)


    return render_template('error.html')


@app.route('/ansible', methods=['POST'])
def ansible():
    global peticion
    global nombre_path
    global path

    tipoPeticion = request.form['selectTarea']
    nombreArchivo = request.form['nombreElemento']

    session = Models.Session.getInstance()
    nombreUsuario = session.getlogedUser().nombreUsuario

    peticion= tipoPeticion
    nombre_path= path+nombreArchivo

    ansibleFuntion()

    cursor = cnx.cursor()
    cursor.callproc("Insertar_Historial_Procedimiento",
                    args=(str(tipoPeticion), str(nombreUsuario)))
    cnx.commit()

    return render_template('success.html')



if __name__ == '__main__':
    app.run(port=8090, debug=True)


cnx.close()