from flask import Flask,render_template 
import requests

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

app =Flask (__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///POKEDEX.sqlite"

db = SQLAlchemy(app)

class pokemon(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(db.String, nullable=False)
    height: Mapped[float] = mapped_column(db.Float, nullable=False)
    weight: Mapped[float] = mapped_column(db.Float, nullable=False)
    order: Mapped[int] = mapped_column(db.Integer, nullable=False)
    type:  Mapped[str] = mapped_column(db.String, nullable=False)


with app.app_context():
     db.create_all()


def get_pokemon_data(pokemon):
    url= f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    r= requests.get(url).json()
    return r


@app.route("/")
def home():
    data = get_pokemon_data('lucario')
    pokemon= {
            'id':data.get('name'),
              'name':data.get('name'),
              'height':data.get('height'),
              'weight':data.get('weight'), 
              'order': data.get('weight'),
              'type': 'agua',
              'photo': data.get('sprites').get('other').get('official-artwork').get('front_default')
                    }
    return render_template('pokemon.html', pokemon=pokemon)



@app.route('/insert')
def new_pokemon():
    new_pokemon = 'pikachu'
    if new_pokemon:
          obj = pokemon(name= new_pokemon, height=1.50,weight= 60, order=100,type= 'electrico' ) 
          db.session.add(obj)
          db.session.commit()
    return 'Pokemon Agregado'


@app.route('/select')
def select():
    Lista_pokemon = pokemon.query.all()
    for p in Lista_pokemon:
        print(p.name)
    return 'alo'

@app.route('/select/<name>')
def selectbyname(name):
    poke= pokemon.query.filter_by(name=name).first()
    return str(poke.id) + str(poke.name)

@app.route('/selectbyid/<id>')
def selectbyid(id):
    poke= pokemon.query.filter_by(id=id).first()
    return str(poke.id) + str(poke.name)


@app.route('/deletebyid/<id>')
def deletebyid(id):
    poke_eliminado= pokemon.query.filter_by(id=id).first()
    db.session.delete(poke_eliminado)
    db.session.commit()
    return 'Pokemon Eliminado'



if __name__=='__main__':
    app.run(debug=True)
