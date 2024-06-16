import os
from flask import request
import pandas as pd
import json


def registryRouter(app, model):

    @app.route("/train", methods=["POST"])
    def Audio2Text():
        try:
            model.train()
            return {"status": "success", "data": "ok"}, 200
        except:
            return {"status": "success", "data": "Could not detect lyrics"}, 400

    @app.route("/predict", methods=["POST"])
    def recommend():
        try:
            userId = request.json["userId"]
            data = model.predict(userId)
            return {"status": "success", "data": data}, 200
        except Exception as e:
            print(e)
            return {"status": "success", "data": "Something went wrong"}, 400

    @app.route("/movies/<movieId>", methods=["GET"])
    def movies(movieId=None):
        try:

            meta_name = "meta_Movies_and_TV.json"
            current_dir = os.path.dirname(os.path.realpath(__file__))
            data_path = os.path.join(current_dir, "..", "resources", "slirec")
            meta_file = os.path.join(data_path, meta_name)
            meta_r = open(meta_file, "r")

            for line in meta_r:
                line_new = eval(line)
                if line_new["asin"] == movieId:
                    return {"status": "success", "data": line_new}, 200

            return {"status": "filed", "data": "Movie not found"}, 404

        except Exception as e:
            print(e)
            return {"status": "filed", "data": "Something went wrong"}, 400
