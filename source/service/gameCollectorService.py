from flask import Flask, jsonify, json, Response, request
from flask_cors import CORS, cross_origin

import logging
import gameTableClient
import sys

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

CORS(app)

@app.route("/")
def healthCheckResponse():
    return jsonify({"message" : "Nothing here, used for health check. Try /collection instead."})

@app.route("/collection", methods=['GET'])
def getGames():
    app.logger.info('GAME COLLECTION LOGGER')
    serviceResponse = gameTableClient.getAllGames()

    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"

    return flaskResponse

@app.route("/collection/<gameID>", methods=['GET'])
def getGame(gameID):
    app.logger.info('GAME COLLECTION GET GAME LOGGER')
    serviceResponse = gameTableClient.getGame(gameID)

    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"

    return flaskResponse

@app.route("/collection/add", methods=['POST'])
@cross_origin()
def addGame():
    app.logger.info('ADD GAME LOGGER')
    
    data = request.json;
    app.logger.info(data);
    
    serviceResponse = gameTableClient.addGame(data)
    
    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"

    return flaskResponse;
    
@app.route("/collection/<gameID>/delete", methods=['POST'])
@cross_origin()
def deleteGame(gameID):
    app.logger.info('DELETE GAME LOGGER')
    
    app.logger.info("Game ID is " + gameID);
    
    serviceResponse = gameTableClient.deleteGame(gameID)
    
    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"

    return jsonify(gameID);
    
@app.route("/collection/update", methods=['POST'])
@cross_origin()
def updateGame():
    app.logger.info('UPDATE GAME LOGGER')
    
    data = request.json;
    app.logger.info(data);
    
    serviceResponse = gameTableClient.updateGame(data)
    
    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"

    return jsonify(data);
    
@app.route("/collection/profile/register/<email>", methods=['POST'])
@cross_origin()
def registerUser(email):
    app.logger.info('PROFILE LOGGER')
    
    app.logger.info(email)
    
    serviceResponse = gameTableClient.registerUser(email)
    
    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"

    return flaskResponse;
    
@app.route("/collection/profile/<email>", methods=['GET'])
def getProfileID(email):
    app.logger.info('GET PROFILE ID LOGGER')

    app.logger.info('I received the email: ' + email)    
    serviceResponse = gameTableClient.getProfileID(json.dumps(email))

    app.logger.info(jsonify(serviceResponse));
    
    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"

    return flaskResponse
    
@app.route("/collection/rank/<profileID>", methods=['GET'])
def getOwnedGames(profileID):
    app.logger.info('RANK GAMES LOGGER')
    serviceResponse = gameTableClient.getOwnedGames(profileID)

    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"

    return flaskResponse
    
@app.errorhandler(Exception)
def handleError(error):
    return error;
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
