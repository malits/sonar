from flask import Flask, jsonify, request, render_template
import tensorflow as tf

from model_handler import ModelHandler

app = Flask(__name__, instance_relative_config=False)


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


@app.route('/send_message', methods=["POST"])
def process_message():
    global graph
    with graph.as_default():
        data = request.get_json()
        handler.predict_sentiment(data["message"])
        return 'OK', 200


@app.route('/get_probability')
def get_probability():
    return str(handler.get_prob())


if __name__ == '__main__':
    global handler
    handler = ModelHandler()
    graph = tf.get_default_graph()
    app.run()
