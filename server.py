from flask import Flask, jsonify, request, render_template
from model_handler import ModelHandler


def create_app():
    app = Flask(__name__, instance_relative_config=False)

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
                "score": handler.predict_sentiment(data["message"]),
            })

    @app.route('/')
    def hello():
        return render_template("index.html")

    @app.route('/send_message', methods=["POST"])
    def process_message():
        data = request.get_json()
        handler.predict_sentiment(data["message"])

    @app.route('/get_probability')
    def get_probability():
        return str(handler.get_prob())

    return app
