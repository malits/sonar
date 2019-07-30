from flask import Flask, jsonify, request, render_template
import tensorflow as tf

from model_handler import ModelHandler

app = Flask(__name__, instance_relative_config=False)


def load_model():
    global handler
    handler = ModelHandler()


@app.route('/test', methods=["POST", "GET"])
def process_request():

    # POST request
    if request.method == "POST":
        print(request.content_type)
        data = request.get_json()
        print(data['message'])
        return 'OK', 200

    # GET request
    elif request.method == "GET":
        return jsonify({
            "score": data['message'],
        })


@app.route('/')
def hello():
    return render_template("index.html")


@app.route('/predict')
def predict():
    data = request.get_json()
    return handler.predict_sentiment(data["message"])


if __name__ == '__main__':
    load_model()
    app.run()
