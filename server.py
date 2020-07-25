from flask import Flask, render_template, request, session, Response, redirect, jsonify
from flask_cors import CORS
from database import connector
from model import entities
from werkzeug.utils import secure_filename
import json
import time
import os


db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/albergue', methods=['POST'])
def create_albergue():
    create = json.loads(request.form['data'])
    files = request.files
    session = db.getSession(engine)
    usuario = entities.Usuario(
        nombre = create["admin"]["nombre"],
        apellidos = create["admin"]["apellidos"],
        representante = create["admin"]["representante"],
        celular = create["admin"]["celular"],
        correo = create["admin"]["correo"],
        contrasenha = create["admin"]["contrasenha"]
    )
    session.add(usuario)
    session.flush()
    albergue = entities.Albergue(
        admin_id = usuario.id,
        nombre = create["albergue"]["nombre"],
        anios = create["albergue"]["anios"],
        direccion = create["albergue"]["direccion"],
        urbanizacion = create["albergue"]["urbanizacion"],
        distrito = create["albergue"]["distrito"],
        ciudad = create["albergue"]["ciudad"],
        departamento = create["albergue"]["departamento"],
        tamanio = create["albergue"]["tamanio"],
        material = create["albergue"]["material"],
        gasto = create["albergue"]["gasto"],
        pertenencia = create["albergue"]["pertenencia"],
        voluntarios = create["albergue"]["voluntarios"],
        albergan = create["albergue"]["albergan"],
        num_gatos = create["albergue"]["num_gatos"],
        acep_donaciones = create["albergue"]["acep_donaciones"],
        acep_apoyo = create["albergue"]["acep_apoyo"],
        banco_name = create["albergue"]["banco_name"],
        banco_number = create["albergue"]["banco_number"],
        banco_cci = create["albergue"]["banco_cci"],
        facebook = create["albergue"]["facebook"],
        instagram = create["albergue"]["instagram"],
        correo = create["albergue"]["correo"],
        otro_contacto = create["albergue"]["otro_contacto"]
    )
    session.add(albergue)
    session.flush()
    for i in range(6):
        nombre = "gato" + str(i)
        if(create[nombre]["nombre"] != ""):
            gato = entities.Gato(
                albergue_id = albergue.id,
                nombre = create[nombre]["nombre"],
                img = "", #nombre de la imagen 
                edad = create[nombre]["edad"],
                adopcion = create[nombre]["adopcion"]
            )
            session.add(gato)
            session.flush()
            temp = gato.id
            path = '/home/ubuntu/flaskapp'
            os.mkdir(path + "/gatos_imgs/" + str(gato.id))
            foto = files['files[' + str(i) + ']']
            print(foto.filename)
            nombre_foto = secure_filename(foto.filename)
            foto.save(path+"/gatos_imgs/"+str(gato.id)+"/"+ nombre_foto)
            session.commit()
            actualizar = session.query(entities.Gato).filter(entities.Gato.id == temp).first()
            setattr(actualizar, 'img', path+"/gatos_imgs/"+str(gato.id)+"/"+ nombre_foto)
            session.commit()
    session.commit()
    session.close()
    return "finalizado la insercion de datos"

@app.route('/get_gatos/<id>', methods = ['GET'])
def search_gatos(id):
    _id = int(id)
    db_session = db.getSession(engine)
    gatos_from_id = db_session.query(entities.Gato).filter(entities.Gato.albergue_id == _id)
    db_session.close()
    gatos = gatos_from_id[:]
    msg = {'gatos':gatos}
    return Response(json.dumps(msg, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/get_gatos', methods = ['GET'])
def get_gatos():
    db_session = db.getSession(engine)
    gatos_from_id = db_session.query(entities.Gato)
    gatos = gatos_from_id[:]
    gatos_inst = []
    for gato in gatos:
        gato_inst = {}
        albergue = db_session.query(entities.Albergue).filter(entities.Albergue.id == gato.albergue_id).first()
        gato_inst['albergue'] = albergue.nombre
        gato_inst['nombre'] = gato.nombre
        gato_inst['edad'] = gato.edad
        gato_inst['adopcion'] = gato.adopcion
        gato_inst['img'] = gato.img
        gatos_inst.append(gato_inst)
    db_session.close()
    msg = { 'gatos': gatos_inst }
    return Response(json.dumps(msg, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/get_albergues', methods = ['GET'])
def search_albergues():
    db_session = db.getSession(engine)
    dbResponse = db_session.query(entities.Albergue)
    albergues = dbResponse[:]#nombre del representante, telefono, nombre del albergue, albergan, ciudad, anios, numgatos, facebook, instagram, correo
    lbrgs_rspns = []
    for albergue in albergues:
        admin = db_session.query(entities.Usuario).filter(entities.Usuario.id == albergue.admin_id)
        admin = admin[:]
        admin = admin[0]
        res = {
            'nombre':admin.nombre + ' ' + admin.apellidos,
            'telefono': admin.celular,
            'nombre_albergue':albergue.nombre,
            'albergan':albergue.albergan,
            'cuidad':albergue.ciudad,
            'anios':albergue.anios,
            'num_gatos': albergue.num_gatos,
            'facebook': albergue.facebook,
            'instagram': albergue.instagram,
            'correo': albergue.correo
        }
        lbrgs_rspns.append(res)
    return Response(json.dumps(lbrgs_rspns, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/borrar')
def borrar():
    db.destroyTables(engine)

@app.route('/delete_gato/<id>', methods=['DELETE'])
def delete_gato(id):
    _id = int(id)
    session = db.getSession(engine)
    msg = session.query(entities.Gato).filter(entities.Gato.id == _id).one()
    session.delete(msg)
    session.commit()
    session.close()
    return "Gato borrado"
    #crear gato, creo un file con el nombre de la carpeta 

@app.route('/authenticate/<correo>/<contrasenha>', methods=['POST'])
def login(correo, contrasenha): 
    #print(request.data)
    #compare = json.loads(request.data)
    session = db.getSession(engine) 
    msg = session.query(entities.Usuario).filter(entities.Usuario.correo == correo).filter(entities.Usuario.contrasenha == contrasenha).first()
    session.close()
    if(msg):
        message = {'message': 'Authorized'}
        return Response(message, status=200, mimetype='application/json')
    else:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')


@app.route('/contact', methods=['POST'])
def set_contactos():
    create = json.loads(request.data)
    ctct = entities.Contacto(
               nombre = create["nombre"],
               apellidos = create["apellidos"],
               celular = create["celular"],
               correo = create["correo"],
               mensaje = create["mensaje"]
            )
    session=db.getSession(engine)
    session.add(ctct)
    session.commit()
    session.close()
    return "se creo bn"


@app.route('/', methods=['GET'])
def get_index():
    return "HOLA YA SE SUBIO"


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('0.0.0.0'))
