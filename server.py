from flask import Flask, jsonify, request, render_template
import tensorflow as tf

from models.neural import SentimentAnalyzer

app = Flask(__name__, instance_relative_config=False)


def load_model():
    global model
    model = SentimentAnalyzer()
    model.load_model()


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


@app.route('/predict', methods=["POST", "GET"])
def predict():
    global graph
    with graph.as_default():
        data = request.get_json()
        message = data["message"]
        response = {"prob": str(model.predict_sentiment([message])[0][0])}
        return jsonify(response)


if __name__ == '__main__':
    load_model()
    graph = tf.get_default_graph()

    app.run()
