from distutils.log import info
from flask import Flask, render_template, request, url_for, redirect, jsonify, Response
import requests
from flask_sqlalchemy import SQLAlchemy
import logging
import json, os
from pywebpush import webpush, WebPushException

app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

DER_BASE64_ENCODED_PRIVATE_KEY_FILE_PATH = os.path.join(os.getcwd(),"private_key.txt")
DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH = os.path.join(os.getcwd(),"public_key.txt")

VAPID_PRIVATE_KEY = open(DER_BASE64_ENCODED_PRIVATE_KEY_FILE_PATH, "r+").readline().strip("\n")
VAPID_PUBLIC_KEY = open(DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH, "r+").read().strip("\n")

VAPID_CLAIMS = {
"sub": "mailto:develop@raturi.in"
}

def send_web_push(subscription_information, message_body):
    return webpush(
        subscription_info=subscription_information,
        data=message_body,
        vapid_private_key=VAPID_PRIVATE_KEY,
        vapid_claims=VAPID_CLAIMS
    )


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tasks.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/registrationdoc')
def doc():

    return render_template('registrationdoc.html')

@app.route('/login')
def login():

    return render_template('login.html')

@app.route('/formulario')
def formulario():

    return render_template('formulario.html')

@app.route('/paciente')
def paciente():
    print('si')
    return render_template('paciente.html')

@app.route('/quien')
def quienes():

    return render_template('quienes_somos.html')

# Para ingresar CI y ver datos

@app.route('/cargado', methods=['POST', 'GET'])
def cargado():
    if request.method == 'POST':
        cedula = request.form["cedula"]
        user = Task.query.filter_by(cedula=cedula).first()
        return render_template('usuario.html', user=user)
    return render_template('formulario_cargado.html')

@app.route('/buscar')
def buscar():
    cedula = request.form['cedula']
    return render_template('formulario.html')

#Base de datos

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(300))
    apellido = db.Column(db.String(300))
    cedula = db.Column(db.Integer)
    ciudad = db.Column(db.String(300))
    correo = db.Column(db.String(300))
    fecha = db.Column(db.Integer)    
    motivo_de_consulta = db.Column(db.String(300))
    diagnostico = db.Column(db.String(300))
    indicaciones = db.Column(db.String(300))
    receta_1 = db.Column(db.String(300))
    receta_2 = db.Column(db.String(300))


@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('index.html', tasks = tasks)

@app.route('/formulario')
def form():
    tasks = Task.query.all()
    return render_template('formulario.html', tasks = tasks)

@app.route('/create-task', methods=['POST'])
def create():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    cedula = request.form['cedula']
    ciudad = request.form['ciudad']
    correo = request.form['correo']
    fecha = request.form['fecha']
    motivo_de_consulta = request.form['motivo_de_consulta']
    diagnostico = request.form['diagnostico']
    indicaciones = request.form['indicaciones']
    receta_1 = request.form['receta_1']
    receta_2 = request.form['receta_2']

    new_task = Task(
        nombre=nombre,
        apellido=apellido,
        cedula=cedula,
        ciudad=ciudad,
        correo=correo,
        fecha=fecha,
        motivo_de_consulta=motivo_de_consulta,
        diagnostico=diagnostico,
        indicaciones=indicaciones,
        receta_1=receta_1,
        receta_2=receta_2
    )
    
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/done/<id>')
def done(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not(task.done)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<id>')
def delete(id):
    Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/subscription/", methods=["GET", "POST"])
def subscription():
    """
        POST creates a subscription
        GET returns vapid public key which clients uses to send around push notification
    """

    if request.method == "GET":
        return Response(response=json.dumps({"public_key": VAPID_PUBLIC_KEY}),
            headers={"Access-Control-Allow-Origin": "*"}, content_type="application/json")

    subscription_token = request.get_json("subscription_token")
    return Response(status=201, mimetype="application/json")

@app.route("/push_v1/",methods=['POST'])
def push_v1():
    message = "TU HERMANA EN TANGA"
    print("is_json",request.is_json)

    if not request.json or not request.json.get('sub_token'):
        return jsonify({'failed':1})

    print("request.json",request.json)

    token = request.json.get('sub_token')
    try:
        token = json.loads(token)
        send_web_push(token, message)
        return jsonify({'success':1})
    except Exception as e:
        print("error",e)
        return jsonify({'failed':str(e)})

@app.route('/pruebita')
def prueba():
    return render_template('indexo.html')

if __name__ == '__main__':
    app.run(debug=True) 