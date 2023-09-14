from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:administrador123456789@localhost/flask_restapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Club(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    colors = db.Column(db.String(75), nullable=False)
    stadium = db.Column(db.String(150), nullable=False)

    def __init__(self, name, year, colors, stadium):
        self.name = name
        self.stadium = stadium
        self.year = year
        self.colors = colors


class ClubSchema(ma.Schema):
    
    class Meta:
        fields = ('id', 'name', 'year', 'colors', 'stadium')

club_schema = ClubSchema()
clubs_schema = ClubSchema(many=True)

@app.route('/clubs', methods=['POST'])
def create_club():
    name = request.json['name']
    year = request.json['year']
    colors = request.json['colors']
    stadium = request.json['stadium']

    new_club = Club(name, year, colors, stadium)
    db.session.add(new_club)
    db.session.commit()

    return club_schema.jsonify(new_club)

@app.route('/clubs', methods=['GET'])
def get_clubs():
    all_clubs = Club.query.all()
    result = clubs_schema.dump(all_clubs)
    return jsonify(result)

@app.route('/clubs/<id>', methods=['GET'])
def get_club(id):
    club = Club.query.get(id)
    return club_schema.jsonify(club)

# UPDATE DATA.
@app.route('/clubs/<id>', methods=['PUT'])
def update_club(id):
    club = Club.query.get(id)

    name = request.json['name']
    year = request.json['year']
    colors = request.json['colors']
    stadium = request.json['stadium']

    club.name = name
    club.year = year
    club.colors = colors
    club.stadium = stadium

    db.session.commit()
    return club_schema.jsonify(club)

@app.route('/clubs/<id>', methods=['DELETE'])
def delete_club(id):
    club = Club.query.get(id)
    db.session.delete(club)
    db.session.commit()

    return club_schema.jsonify(club)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Bienvenido a mi API, visita: /clubs'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
       