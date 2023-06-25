from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# DATABASE CONFIGURACIONES
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)    

# MODELOS DE LA BASE DE DATOS
class Animal_encontrado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raza = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(300), nullable=False)

class Animal_perdido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raza = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(300), nullable=False)
    
# Descomentar y ejecutar el siguiente codigo unicamente si las tablas no estan creadas todavia, luego volverlas a comentar
# with app.app_context():
#     db.create_all()


@app.route("/")
def index():

    animales_encontrados = Animal_encontrado.query.all()

    diccionario__de_animales = {
        "animales": []
    }

    for animal in animales_encontrados:
        diccionario__de_animales["animales"].append({
            "raza": animal.raza,
            "color": animal.color,
            "ubicacion": animal.ubicacion
        })

    return render_template("index.html", animales_encontrados=json.dumps(diccionario__de_animales))



@app.route("/perro-encontrado", methods=["GET", "POST"])
def encontrado():
    if request.method == "POST":
        raza = request.form["raza"]
        color = request.form["color"]
        ubicacion = request.form["ubicacion"]

        animal_encontrado = Animal_encontrado(raza=raza, color=color, ubicacion=ubicacion)

        with app.app_context():
            db.session.add(animal_encontrado)
            db.session.commit()
    
        return redirect(url_for("index", ubicacion=ubicacion))
    else:
        return render_template("encontrado.html")


# Esta ruta puede manejar tanto requests GET como POST
@app.route("/perro-perdido", methods=["GET", "POST"])
def perdido():

    # Si la request es POST (es POST cuando se envia un formulario):
    if request.method == "POST":
        raza = request.form["raza"]
        color = request.form["color"]
        ubicacion = request.form["ubicacion"]

        # Se cargan los datos del formulario
        animal_perdido = Animal_perdido(raza=raza, color=color, ubicacion=ubicacion)

        # Se los carga a la tabla correspondiente
        with app.app_context():
            db.session.add(animal_perdido)
            db.session.commit()

        # Se redirecciona al index
        return redirect(url_for("index"))
    
    # Si la request es GET (es GET al solamente cargar la pagina)
    else:
        return render_template("perdido.html")

