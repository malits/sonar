from flask import Flask, jsonify, request, render_template


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        # instance config with user data
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    @app.route('/test', methods=["POST", "GET"])
    def process_request():

        # POST request
        if request.method == "POST":
            print('POST request')
            print(request.get_json())
            return 'OK', 200

        # GET request
        elif request.method == "GET":
            print("GET request")
            message = {"test": "This is a test response"}
            return jsonify(message)

    @app.route('/', methods=["POST", "GET"])
    def hello():
        return render_template("index.html", score=3)

    return app
