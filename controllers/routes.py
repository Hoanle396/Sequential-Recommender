from flask import request, render_template
import json


def registryRouter(app, model):

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/train", methods=["POST"])
    def Audio2Text():
        try:
            model.train()
            return {"status": "success", "data": "ok"}, 200
        except:
            return {"status": "failed", "data": "Could not train"}, 400

    @app.route("/load", methods=["GET"])
    def pre_data():
        try:
            model.pre_data()
            return {"status": "success", "data": "ok"}, 200
        except Exception as e:
            print(e)
            return {"status": "failed", "data": "Could not load"}, 400

    @app.route("/predict", methods=["POST"])
    def recommend():
        try:
            userId = request.json["userId"]
            data = model.predict(userId)
            return {"status": "success", "data": data}, 200
        except Exception as e:
            print(e)
            return {"status": "failed", "data": "Something went wrong"}, 400

    @app.route("/movies/<movieId>", methods=["GET"])
    def movies(movieId=None):
        try:
            data = model.get_movies(movieId)
            return {"status": "success", "data": json.loads(data)}, 200

        except Exception as e:
            print(e)
            return {"status": "failed", "data": "Something went wrong"}, 400
