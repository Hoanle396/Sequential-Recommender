from app import app
import app.settings as settings
from controllers.routes import registryRouter
from models.recommender import Recommender

model = Recommender()

if __name__ == "__main__":
    registryRouter(app, model)
    app.run(host=settings.BE_HOST, port=settings.BE_PORT, debug=settings.ENV != "PROD")