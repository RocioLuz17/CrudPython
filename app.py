from flask import Flask,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:@127.0.0.1:3306/articulos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db= SQLAlchemy(app)
ma= Marshmallow(app)

class Articulo (db.Model):
    id= db.Column(db.Integer, primary_key= True)
    serie=db.Column(db.Integer)
    precio=db.Column(db.Integer)
    descripcion=db.Column(db.String(100))
    stock=db.Column(db.Integer)

    def __init__(self,serie,precio,descripcion,stock):
        self.serie= serie
        self.precio= precio
        self.descripcion=descripcion
        self.stock=stock


with app.app_context():
    db.create_all()

class ArticuloSchema(ma.Schema):
     class Meta:
        fields=('id','serie','precio','descripcion','stock')

articulo_schema= ArticuloSchema()
articulos_schema= ArticuloSchema(many=True)


@app.route('/articulos', methods=['GET'])
def get_articulos():
    all_articulos= Articulo.query.all()
    
    return articulos_schema.jsonify(all_articulos)


@app.route('/articulos', methods=['POST'])
def create_articulo():
    serie= request.json['serie'] 
    precio= request.json['precio'] 
    descripcion= request.json['descripcion'] 
    stock= request.json['stock'] 

    new_articulo= Articulo(serie,precio,descripcion,stock)
    db.session.add(new_articulo)
    db.session.commit()
    
    return articulo_schema.jsonify(new_articulo)
  

@app.route('/articuloS/<id>', methods=['GET'])
def get_articulo(id):

    articulo = Articulo.query.get(id)

    return articulo_schema.jsonify(articulo)



@app.route('/articuloS/<id>', methods=['DELETE'])
def delete_articulo(id):
    articulo= Articulo.query.get(id)
    db.session.delete(articulo)
    db.session.commit()
   
    return articulo_schema.jsonify(articulo)
    
  
@app.route('/articuloS/<id>', methods=['PUT'])
def update_articulo(id):
    articulo= Articulo.query.get(id)


    serie=request.json['serie']
    precio=request.json['precio']
    descripcion=request.json['descripcion']
    stock=request.json['stock']

    articulo.serie= serie
    articulo.precio= precio
    articulo.descripcion=descripcion
    articulo.stock= stock

    db.session.commit()

    return articulo_schema.jsonify(articulo)

if __name__=='__main__':
    app.run(debug=True)


    
    


