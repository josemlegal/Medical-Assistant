from distutils.log import info
from flask import Flask, render_template
import requests

app = Flask(__name__)


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

    return render_template('paciente.html')

@app.route('/quien')
def quienes():

    return render_template('quienes_somos.html')