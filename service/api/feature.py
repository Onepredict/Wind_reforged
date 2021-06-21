import datetime
from flask_restful import Resource, request
from database.models import Device, Waveform, Channel, Feature
from database.factory import DatabaseFactory


class FeatureAPI(Resource):
    @classmethod
    def get(cls, site_id, motor_id):
        session = DatabaseFactory.session
        days = request.args.get("days")
        if days is None:
            features = session.query(Feature).filter(motor_id == Feature.motor_id).order_by(Feature.id.desc()).all()
        else:
            days = int(days)
            current_time = datetime.datetime.utcnow()
            from_date = current_time - datetime.timedelta(days=days)
            features = (
                session.query(Feature)
                .filter(motor_id == Feature.motor_id, Feature.acq_time > from_date)
                .order_by(Feature.id.desc())
                .all()
            )
        features.reverse()
        features_list = [
            {
                "id": feature.id,
                "motor_id": feature.motor_id,
                "acq_time": feature.str_acq_time,
                "aspv": feature.aspv,
                "pvm_width": feature.pvm_width,
                "mmcf": feature.mmcf,
                "arpv": feature.arpv,
                "u_3x": feature.u_3x,
                "v_3x": feature.v_3x,
                "w_3x": feature.w_3x,
                "u_rotor": feature.u_rotor,
                "v_rotor": feature.v_rotor,
                "w_rotor": feature.w_rotor,
                "dtcrv1": feature.dtcrv1,
                "dtcrv2": feature.dtcrv2,
                "dtcrv3": feature.dtcrv3,
                "rms_u": feature.rms_u,
                "rms_v": feature.rms_v,
                "rms_w": feature.rms_w,
                "max_current": feature.max_current,
                "min_current": feature.min_current,
                "mean_current": feature.mean_current,
                "u_thd_0": feature.u_thd_0,
                "u_thd_5": feature.u_thd_5,
                "v_thd_0": feature.v_thd_0,
                "v_thd_5": feature.v_thd_5,
                "w_thd_0": feature.w_thd_0,
                "w_thd_5": feature.w_thd_5,
            }
            for feature in features
        ]
        return features_list, 200


class FeatureEntryAPI(Resource):
    @classmethod
    def get(cls, site_id, motor_id, feature_id):
        session = DatabaseFactory.session
        feature = session.query(Feature).filter(motor_id == Feature.motor_id, feature_id == Feature.id).first()
        if feature is None:
            return None, 404
        feature_json = {
            "motor_id": feature.motor_id,
            "acq_time": feature.str_acq_time,
            "aspv": feature.aspv,
            "pvm_width": feature.pvm_width,
            "mmcf": feature.mmcf,
            "arpv": feature.arpv,
            "u_3x": feature.u_3x,
            "v_3x": feature.v_3x,
            "w_3x": feature.w_3x,
            "u_rotor": feature.u_rotor,
            "v_rotor": feature.v_rotor,
            "w_rotor": feature.w_rotor,
            "dtcrv1": feature.dtcrv1,
            "dtcrv2": feature.dtcrv2,
            "dtcrv3": feature.dtcrv3,
            "rms_u": feature.rms_u,
            "rms_v": feature.rms_v,
            "rms_w": feature.rms_w,
            "max_current": feature.max_current,
            "min_current": feature.min_current,
            "mean_current": feature.mean_current,
            "u_thd_0": feature.u_thd_0,
            "u_thd_5": feature.u_thd_5,
            "v_thd_0": feature.v_thd_0,
            "v_thd_5": feature.v_thd_5,
            "w_thd_0": feature.w_thd_0,
            "w_thd_5": feature.w_thd_5,
        }
        return feature_json, 200