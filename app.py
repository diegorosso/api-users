from flask import Flask, request, jsonify #Request se encarga de extrar los datos que el cliente me podria estar enviando.  
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId

app = Flask(__name__) #inicializa flask.
app.config['MONGO_URI'] = 'mongodb+srv://diego2:diego2@cluster0.kqesm.mongodb.net/my-python-db' #base de datos local.
 
mongo = PyMongo(app) #devuelve un objeto para pader manipularlo. es la conexión con la base de datos local.

CORS(app)

db = mongo.db.users #colección de usuarios

@app.route("/")
def index():
    return  "╰(*°▽°*)╯"

@app.route('/users', methods=['POST']) # Crea rutas para crear usuarios 
def createUser():
    
    data = request.get_json()
    if ('name' not in data or data['name'] == '' or 'email' not in data or 'password' not in data):
        return {"msg": "Missing parameters"}, 400
   
   
    id = db.insert_one({         #Guardar datos con metodo Insert
        'name': data['name'],
        'email': data['email'],
        'password': data['password']
     })

    return jsonify(str(id.inserted_id)) #str convierte el objeto en formato string  
                 


@app.route('/users', methods=['GET']) # Crea rutas para obtener usuarios // consultar todos los datos
def getUsers():
    users = []
    try:
        for doc in db.find(): #busqueda de todos los datos y retorna una lista.
            print(doc)
            users.append({
                '_id': str(ObjectId(doc['_id'])), #ID en formato string
                'name': doc['name'],
                'email': doc['email'],
                'password': doc['password']
            })
    except:
        return "No se tar a mongo", 408


    return jsonify(users)

@app.route('/user/<id>', methods=['GET']) # Crea rutas para obtener un usuario 
def getUser(id):
    try:
        user = db.find_one({'_id':ObjectId(id)})
    except:
        return "id no existe", 404
   
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
        'password': user['password']        
    })

@app.route('/users/<id>', methods=['DELETE']) # Crea rutas para eliminar usuarios 
def deleteUser(id):
    db.delete_one({'_id': ObjectId(id)}) #Elimina el primer dato que coincide con la búsqueda. 
    return jsonify({'msg': 'User delete'})

@app.route('/users/<id>', methods=['PUT']) # Crea rutas para poder editar usuario 
def updeteUser(id):
    db.update_one({'_id': ObjectId(id)}, {'$set':{
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }})
    return jsonify({'msg': 'User update'})



if __name__ == "__main__":
    app.run(debug=True) #debug cada vez que hace cambio el código reinicia.
