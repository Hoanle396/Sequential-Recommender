import os
from flask import request


def registryRouter(app, model):
  
    @app.route("/train", methods=["POST"])
    def Audio2Text():
        try:
            model.train()
            return {"status":"success","data":"ok"},200
        except:
            return {"status":"success","data":"Could not detect lyrics"},400
       
    @app.route("/predict", methods=["POST"])
    def recommend():
        try:
            model.predict()
            return {"status":"success","data":"ok"},200
        except Exception as e:
            print(e)
            return {"status":"success","data":"Could not detect lyrics"},400
        
        