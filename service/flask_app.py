from flask import Flask, Blueprint, render_template
import flask_restful

def create_app():
    _app = Flask("flask_app")

    @_app.route('/test_page')
    def test_page():
        return render_template('index.html')

    with _app.app_context():

        # from libs.logger import Logger, info
        # Logger(app=_app, logger_name="flask_app")

        from api.errors import errors

        ## Adding Resource
        wind_api_blueprint = Blueprint("wind_api", __name__, url_prefix="/api")
        wind_api = flask_restful.Api(wind_api_blueprint, errors=errors)

        ## 
        from api.test import TestAPI
        wind_api.add_resource(TestAPI, "/test")
        _app.register_blueprint(wind_api_blueprint)
    return _app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=4002, use_reloader=True, use_debugger=False, threaded=True)