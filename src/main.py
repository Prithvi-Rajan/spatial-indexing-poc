from flask import Flask
from nearby import Nearby
from flask_restful import Api


app = Flask(__name__)
api = Api(app)



api.add_resource(Nearby, '/nearby')

if __name__ == '__main__':
    app.run()
