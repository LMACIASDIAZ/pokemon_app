from flask import Flask,render_template, request

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

app =Flask (__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///POKEDEX.sqlite"

db = SQLAlchemy(app)

class pokemon(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(db.String, nullable=False)

with app.app_context():
     db.create_all()


def get_pokemon_data(pokemon):
    url= f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    r= request.get (url).json()
    return r


@app.route("/")
def home():
    return render_template('pokemon.html')



@app.route('/insert')
def new_pokemon():
    new_pokemon = 'pikachu'
    if new_pokemon:
          obj = pokemon(name= new_pokemon) 
          db.session.add(obj)
          db.session.commit()
    return 'Pokemon Agregado'


@app.route('/select')
def select():
    Lista_pokemon = pokemon.query.all()
    for p in Lista_pokemon:
        print(p.name)
    return 'pokemon'

@app.route('/select/<name>')
def selectbyid(name):
    poke= pokemon.query.filter_by(name=name).first()
    return str(poke.id)



if __name__=='__main__':
    app.run(debug=True)
