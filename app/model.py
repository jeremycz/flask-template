from flask import Blueprint
from flask import current_app
from flask import request


bp = Blueprint("model", __name__, url_prefix="/model")


class Model():
    def __init__(self) -> None:
        self.ready = False
        self.model = None

    def load(self, path: str = None) -> None:
        """Load the model here"""
        self.ready = True

    def predict(self, query: str = None) -> dict():
        """Method to get a prediction from the model"""
        return dict()


# https://overiq.com/flask-101/application-structure-and-blueprint-in-flask/

model_name = current_app.config.get("MODEL_NAME", None)

model = Model()
model.load(model_name)


@bp.route("/status", methods="GET")
def status():
    return { "loaded": model.ready }


@bp.route("/load", methods="POST")
def load():
    if request.method == "POST":
        model_path = request.args.get("model_path", None)
        if model_path is not None:
            model.load(model_path)


@bp.route("/predict", methods="POST")
def predict():
    """"""
    response = None
    if request.method == "POST":
        user_input = request.args.get("user_input", None)
        if user_input is not None:
            response = model.predict(user_input)
        
    return { "response": response }
