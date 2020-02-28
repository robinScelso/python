from flask import Flask
from flask_restx import Api, Resource, fields, marshal
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app=app, version='0.1', title='meteo Api', description='', validate=True)
ns = api.namespace('meteos', description=' ')

dbclient = MongoClient("mongodb://localhost:27010")
collection = dbclient.meteo

model = api.model('meteo',{
    'id_station': fields.String(readonly=True), 
    'id_sonde': fields.String(readonly=True),
    'latitude': fields.Float(readonly=True),
    'longitude': fields.Float(readonly=True),
    'ville': fields.String(readonly=True),
    'timestamp': fields.String(readonly=True),
    'temperature': fields.Float(readonly=True),
    'humidite': fields.Float(readonly=True)
})

@ns.route('/meteo')
class List(Resource):
    @ns.doc('meteo')
    @ns.marshal_with(model, True)
    def get(self):
        data = collection.find({}, {"_id" : 0})
        data_parsed = []
        for i in data:
            data_parsed.append(i)
        print(data_parsed)
        return data_parsed

    @ns.doc('create_meteo')
    @ns.expect(model)
    @ns.marshal_with(model, code=201)
    def post(self):
        id_res = collection.insert_one(api.api_payload).inserted_id
        result = collection.find_one({"_id" : id_res}, {"_id" : 0})
        return result

if __name__ == '__main__':
    app.run(debug=True)