from flask import Flask, Blueprint
import flask_restful

def create_app():
    _app = Flask("flask_app")

    with _app.app_context():

        from libs.logger import Logger, info
        Logger(app=_app, logger_name="flask_app")

        from api.errors import errors

        ## Adding Resource
        device_api_blueprint = Blueprint("device_api", __name__, url_prefix="/api")
        device_api = flask_restful.Api(device_api_blueprint, errors=errors)

        # device
        device_api.add_resource(DeviceAPI, "/devices")
        device_api.add_resource(DeviceEntryAPI, "/devices/<int:device_id>")

        device_api.add_resource(WaveformAPI, "/devices/<int:device_id>/waveforms")
        device_api.add_resource(WaveformEntryAPI, "/devices/<int:device_id>/waveforms/<int:waveform_id>")

        _app.register_blueprint(device_api_blueprint)

        # motor
        motor_api_blueprint = Blueprint("motor_api", __name__, url_prefix="/api/v1")
        motor_api = flask_restful.Api(motor_api_blueprint, errors=errors)

        motor_api.add_resource(SiteAPI, "/sites")
        motor_api.add_resource(SiteEntryAPI, "/sites/<int:site_id>")
        motor_api.add_resource(SiteStatusAPI, "/sites/<int:site_id>/status")

        motor_api.add_resource(MotorAPI, "/sites/<int:site_id>/motors")
        motor_api.add_resource(MotorEntryAPI, "/sites/<int:site_id>/motors/<int:motor_id>")
        motor_api.add_resource(MotorModelAPI, "/sites/<int:site_id>/motors/<int:motor_id>/model")
        motor_api.add_resource(ParamAPI, "/sites/<int:site_id>/motors/<int:motor_id>/param")
        motor_api.add_resource(FeatureAPI, "/sites/<int:site_id>/motors/<int:motor_id>/features")
        motor_api.add_resource(FeatureEntryAPI, "/sites/<int:site_id>/motors/<int:motor_id>/features/<int:feature_id>")
        motor_api.add_resource(DiagnosisAPI, "/sites/<int:site_id>/motors/<int:motor_id>/diagnosis")
        motor_api.add_resource(
            DiagnosisEntryAPI, "/sites/<int:site_id>/motors/<int:motor_id>/diagnosis/<int:diagnosis_id>"
        )
        motor_api.add_resource(EnergyAPI, "/sites/<int:site_id>/motors/<int:motor_id>/energies")
        motor_api.add_resource(EnergyEntryAPI, "/sites/<int:site_id>/motors/<int:motor_id>/energies/<int:energy_id>")
        motor_api.add_resource(MotorHistoryAPI, "/sites/<int:site_id>/motors/<int:motor_id>/history")

        motor_api.add_resource(HealthCheckAPI, "/healthcheck")
        _app.register_blueprint(motor_api_blueprint)

    return _app


if __name__ == "__main__":
    app = create_app(db_config.ProductionRemoteDBConfig)
    app.run(host="0.0.0.0", port=4002, use_reloader=True, use_debugger=False, threaded=True)